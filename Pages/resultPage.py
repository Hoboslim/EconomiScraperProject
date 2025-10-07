import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

class ResultPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.results_folder = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "ClassificationResults"
        )

        ctk.CTkLabel(self, text="Classification Results", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        ctk.CTkButton(self, text="Select Result CSV", command=self.load_csv).pack(pady=5)
        
        tree_frame = ctk.CTkFrame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        
        self.tree = ttk.Treeview(tree_frame, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")

        
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.grid(row=0,column=1, sticky="ns")
        scrollbar_x.grid(row=1,column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        
        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

       
        ctk.CTkLabel(self, text="Full Article Summary:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        text_frame = ctk.CTkFrame(self)
        text_frame.pack(fill="both", expand=False, padx=10, pady=10)
        
        self.text_box = ctk.CTkTextbox(text_frame, height=150, wrap="word")
        self.text_box.pack(side="left", fill="both", expand=True)
        
        text_scroll = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_box.yview)
        self.text_box.configure(yscrollcommand=text_scroll.set)
        text_scroll.pack(side="right", fill="y")

        ctk.CTkButton(self, text="Back to Home", command=lambda: controller.show_frame("StartPage")).pack(pady=10)

       
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

            self.text_box.delete("1.0", ctk.END)

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

        self.text_box.delete("1.0", ctk.END)
        self.text_box.insert(ctk.END, summary)
