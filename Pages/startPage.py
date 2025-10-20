import customtkinter as ctk
from PIL import Image, ImageTk



class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ctk.CTkButton(self, text="🔆/🌙", fg_color="transparent", command=self.change_mode).pack(pady=10)
        
        ctk.CTkLabel(self, text="Welcome to Webscraper!", font=ctk.CTkFont(size=24, weight="bold", underline=True)).pack(pady=10, padx=10)
        ctk.CTkLabel(self, text="This app lets you scrape articles and classify them using AI.", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        ctk.CTkButton(self, text="Click here to read more!", command=lambda:controller.show_frame("ReadMePage")).pack(pady=10)
        
        self.current_mode = "dark"

        
        startpage_image = ctk.CTkImage(dark_image=Image.open("Images/scraping.jpg"), size=(800, 500))
        ctk.CTkLabel(self,text="", image=startpage_image).pack(pady=5, padx=5)

        ctk.CTkLabel(self, text="© 2025 Webscraper", font=ctk.CTkFont(size=12)).pack(side="bottom")

    
    def change_mode(self):
        if  self.current_mode == "dark":
            ctk.set_appearance_mode("light")
            self.current_mode = "light"
        else:
            ctk.set_appearance_mode("dark")
            self.current_mode = "dark"
            


    
   
        
        