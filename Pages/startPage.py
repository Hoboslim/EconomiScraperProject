import tkinter as tk



class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        
        tk.Label(self, text="Welcome to Webscraper!", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self, text="This app lets you scrape articles and classify them using AI.", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Button(self, text="Go to Scraper Page", command=lambda: controller.show_frame("ScraperPage")).pack(pady=10)
        tk.Button(self, text="Go to Classification Page", command=lambda: controller.show_frame("ClassificationPage")).pack(pady=10)
        tk.Button(self, text="Go to Result Page", command=lambda: controller.show_frame("ResultPage")).pack(pady=10)
        
        