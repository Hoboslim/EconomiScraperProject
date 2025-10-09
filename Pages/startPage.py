import customtkinter as ctk



class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        
        ctk.CTkLabel(self, text="Welcome to Webscraper!", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self, text="This app lets you scrape articles and classify them using AI.", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        ctk.CTkButton(self, text="Go to Scraper Page", command=lambda: controller.show_frame("ScraperPage")).pack(pady=10)
        ctk.CTkButton(self, text="Go to Classification Page", command=lambda: controller.show_frame("ClassificationPage")).pack(pady=10)
        ctk.CTkButton(self, text="Go To Analysis Page", command=lambda: controller.show_frame("AnalysisPage")).pack(pady=10)
        ctk.CTkButton(self, text="Go to Result Page", command=lambda: controller.show_frame("ResultPage")).pack(pady=10)
        
        