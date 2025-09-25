import tkinter as tk
from tkinter import ttk, messagebox
import os, subprocess
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
        
    def run_scraper(self):
        selected_scraper = self.dropdown.get()
        if selected_scraper:
            filepath = os.path.join(self.folder, selected_scraper)
        try:
            subprocess.run(["python", filepath], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running this file: {e}")

        
        
        