import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.results_folder = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "ClassificationResults"
        )

        tk.Label(self, text="Classification Results", font=("Arial", 18, "bold")).pack(pady=10)
        tk.Button(self, text="Select Result CSV", command=self.load_csv).pack(pady=5)

        
        self.tree = ttk.Treeview(self, show="headings")
        self.tree.pack(fill="both", expand=True, pady=5)

        
        scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        
        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

       
        tk.Label(self, text="Full Article Summary:", font=("Arial", 14, "bold")).pack(pady=5)
        self.text_box = tk.Text(self, height=10, wrap="word")
        self.text_box.pack(fill="both", expand=False, padx=10, pady=5)
        text_scroll = ttk.Scrollbar(self, orient="vertical", command=self.text_box.yview)
        self.text_box.configure(yscrollcommand=text_scroll.set)
        text_scroll.pack(side="right", fill="y")

        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("StartPage")).pack(pady=10)

       
        self.df = None

    def load_csv(self):
        file_path = filedialog.askopenfilename(
            initialdir=self.results_folder,
            title="Select Classification Result CSV",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            self.df = pd.read_csv(file_path)
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = list(self.df.columns)

            for col in self.df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=150, anchor="w")

            for idx, row in self.df.iterrows():
                self.tree.insert("", "end", iid=idx, values=list(row))

            self.text_box.delete("1.0", tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")

    def on_row_selected(self, event):
        """When a row is clicked, show the full text of the summary."""
        selected = self.tree.selection()
        if not selected or self.df is None:
            return

        idx = int(selected[0])
       
        if "model_summary" in self.df.columns:
            summary = self.df.at[idx, "model_summary"]
        else:
           
            summary = " | ".join(str(self.df.at[idx, col]) for col in self.df.columns)

        self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, summary)
