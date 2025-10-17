import customtkinter as ctk
from tkinter import ttk, messagebox
import os, subprocess, threading
from .classificationPage import ClassificationPage


class ScraperPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="Scraper Page", font=("Arial", 18, "bold")).pack(pady=20)
        
        folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Scrapers")
        self.folder = folder
        options = [fname for fname in os.listdir(folder) if fname.endswith(".py")]
        
        self.dropdown_var = ctk.StringVar()
        self.dropdown = ctk.CTkOptionMenu(self, values=options, variable=self.dropdown_var)
        if options:
            self.dropdown_var.set(options[0])
        self.dropdown.pack(pady=10)
        
        ctk.CTkButton(self, text="Run Scraper", command=self.run_scraper).pack(pady=10)
        
        self.progress = ctk.CTkProgressBar(self, mode="indeterminate", width=250)
        self.progress.set(0)
        self.progress.pack(pady=10)
        
        
        
    def run_scraper(self):
        selected_scraper = self.dropdown.get()
        if not selected_scraper:
            messagebox.showwarning("No Selection", "Please select a scraper first.")
            return
          
            
            
        filepath = os.path.join(self.folder, selected_scraper)
            

        self.progress.start()
        
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
        
        