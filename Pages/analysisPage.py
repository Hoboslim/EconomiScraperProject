import customtkinter as ctk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd


class AnalysisPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Data Analysis", font=("Arial", 18, "bold")).pack(pady=20)

        ctk.CTkButton(self, text="Select CSV File", command=self.load_csv).pack(pady=10)

        self.column_var = ctk.StringVar()
        self.column_dropdown = ctk.CTkOptionMenu(self, values=[], variable=self.column_var)
        self.column_dropdown.pack(pady=10)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=5)

        ctk.CTkButton(button_frame, text="Show Bar Chart", command=self.show_bar_chart).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Show Pie Chart", command=self.show_pie_chart).grid(row=0, column=1, padx=5, pady=5)

        self.canvas = None
        self.figure = None

        self.df = None
        self.allowed_columns = ["Model_category", "Time", "Sentiment"]
        self.column_mapping = {
            "Model_category": ["Model_Category", "Model_category", "Model", "model_category"],
            "Time": ["Time (s)", "Time", "time_stamp", "DateTime", "time"],
            "Sentiment": ["Sentiment", "sentiment"]
        }

    def load_csv(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return
        try:
            self.df = pd.read_csv(filepath)
            messagebox.showinfo("Success", f"Loaded {filepath.split('/')[-1]} successfully!")

            available = []
            for col in self.allowed_columns:
                for variant in self.column_mapping[col]:
                    if variant in self.df.columns:
                        available.append(variant)
                        break

            if available:
                self.column_dropdown.configure(values=available)
                self.column_var.set(available[0])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV file:\n{e}")

    def clear_plot(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
            self.figure = None

    def show_bar_chart(self):
        if not self._check_ready(): return
        col = self.column_var.get()
        self.clear_plot()
        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        ax = self.figure.add_subplot(111)
        self.df[col].value_counts().plot(kind='bar', ax=ax, color='lightgreen', edgecolor='black')
        ax.set_title(f"Bar Chart of {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        self._embed_plot()

    def show_pie_chart(self):
        if not self._check_ready(): return
        col = self.column_var.get()
        self.clear_plot()
        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        ax = self.figure.add_subplot(111)
        self.df[col].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90)
        ax.set_ylabel('')
        ax.set_title(f"Pie Chart of {col}")
        self._embed_plot()

    def _embed_plot(self):
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def _check_ready(self):
        if self.df is None:
            messagebox.showwarning("No CSV", "Please load a CSV file first.")
            return False
        if not self.column_var.get():
            messagebox.showwarning("No Column", "Please select a column first.")
            return False
        return True
