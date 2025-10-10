import customtkinter as ctk
from PIL import Image, ImageTk



class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        ctk.CTkLabel(self, text="Welcome to Webscraper!", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=20, padx=20)
        ctk.CTkLabel(self, text="This app lets you scrape articles and classify them using AI.", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        ctk.CTkButton(self, text="Click here to read more!", command=lambda:controller.show_frame("ReadMePage")).pack(pady=10)

        startpage_image = ctk.CTkImage(dark_image=Image.open("Images/scraping.jpg"), size=(800, 500))
        ctk.CTkLabel(self,text="", image=startpage_image).pack(pady=10)

        ctk.CTkLabel(self, text="© 2025 Webscraper", font=ctk.CTkFont(size=14)).pack(side="bottom", pady=10)
        
        