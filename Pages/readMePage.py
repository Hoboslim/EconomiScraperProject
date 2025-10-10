import customtkinter as ctk

class ReadMePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Instructions", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=10)
        ctk.CTkLabel(self, text="How to use Webscraper:", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=10)
        
        ctk.CTkButton(self, text="Read ME:", command=self.show_readme).pack(pady=10)
        ctk.CTkButton(self, text="Back to Home", command=lambda: controller.show_frame("StartPage")).pack(side="bottom", pady=10)
        
        
       

            



