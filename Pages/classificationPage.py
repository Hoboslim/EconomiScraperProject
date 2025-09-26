import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading
from Classification.ArticleClassifier import run_classification
from .startPage import StartPage

class ClassificationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Label(self, text="Classification Page", font=("Arial", 18, "bold")).pack(pady=20)
        
        self.articles_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Articles")
        self.csv_dropdown = ttk.Combobox(self, values=self.get_csv_files(), state="readonly")
        if self.get_csv_files():
            self.csv_dropdown.current(0)
        self.csv_dropdown.pack(pady=10)
        
        tk.Button(self, text="Run Classification", command=self.run_selected_classification).pack(pady=10)
        tk.Button(self, text="Refresh Articles", command=self.refresh_csv_dropdown).pack(pady=5)
        tk.Button(self, text="Back To Home", command=lambda: controller.show_frame("StartPage")).pack(pady=10)
        
        self.progress = ttk.Progressbar(self, mode="indeterminate", length=250)
        self.progress.pack(pady=10)
        
        
    def get_csv_files(self):
        return [f for f in os.listdir(self.articles_folder) if f.endswith(".csv")]
    
    
    def refresh_csv_dropdown(self):
        files = self.get_csv_files()
        self.csv_dropdown["values"] = files
        if files:
            self.csv_dropdown.current(0)
            
              
    def run_selected_classification(self):
        selected_csv = self.csv_dropdown.get()
        if not selected_csv:
            messagebox.showwarning("No Selection", "Please select a csv file first.")
            return
        
        file_path = os.path.join(self.articles_folder, selected_csv)
        
        self.progress.start(10)
        
        threading.Thread(target=self._run_classification_task, args=(file_path,), daemon=True).start()
    def _run_classification_task(self, file_path):
        try:
            run_classification(file_path)
        except Exception as e:
            print(f"Error running classification {e}")
            messagebox.showerror("Error", "Classification failed: {e}")
        finally:
            
            self.after(0, self.progress.stop)
            self.after(0, lambda: messagebox.showinfo("Done", "Classification finished!"))
     
        