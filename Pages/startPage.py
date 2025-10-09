import customtkinter as ctk



class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        
        ctk.CTkLabel(self, text="Welcome to Webscraper!", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self, text="This app lets you scrape articles and classify them using AI.", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
       
        
        