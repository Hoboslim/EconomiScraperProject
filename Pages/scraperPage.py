import tkinter as tk
from tkinter import ttk, messagebox
import os, subprocess, threading
from .classificationPage import ClassificationPage


class ScraperPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Label(self, text="Scraper Page", font=("Arial", 18, "bold")).pack(pady=20)
        
        folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Scrapers")
        self.folder = folder
        options = [fname for fname in os.listdir(folder) if fname.endswith(".py")]
        
        self.dropdown = ttk.Combobox(self, values=options, state="readonly")
        if options:
            self.dropdown.current(0)
        self.dropdown.pack(pady=10)
        
        tk.Button(self, text="Run Scraper", command=self.run_scraper).pack(pady=10)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("StartPage")).pack(pady=10)
        
        self.progress = ttk.Progressbar(self, mode="indeterminate", length=250)
        self.progress.pack(pady=10)
        
        
        
    def run_scraper(self):
        selected_scraper = self.dropdown.get()
        if not selected_scraper:
            messagebox.showwarning("No Selection", "Please select a scraper first.")
            return
          
            
            
        filepath = os.path.join(self.folder, selected_scraper)
            

        self.progress.start(10)
        
        threading.Thread(target=self._run_scraper_task, args=(filepath,), daemon=True).start()
        
    def _run_scraper_task(self, filepath):
        try:
            subprocess.run(["python", filepath], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running this file: {e}")
            messagebox.showerror("Error" f"scraper failed: {e}")
        finally:
            
            self.after(0, self.progress.stop)
            self.after(0, lambda: messagebox.showinfo("Done", "Scraper Finished!"))
        
        