import customtkinter as ctk
import tkinter as tk
from PIL import Image
from tkinter import Menu
from .startPage import StartPage
from .scraperPage import ScraperPage
from .classificationPage import ClassificationPage
from .resultPage import ResultPage
from .analysisPage import AnalysisPage
from .readMePage import ReadMePage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("themes/scraper_theme.json")
        
        self.title("Webscraper")
        self.iconbitmap("Images/WebScraperLogo.ico")
        self.geometry("600x500")
        self.minsize(600, 500)
      
        self.sidebar = ctk.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar.pack(expand=False, side="left", fill="both", padx=10, pady=10)

        ctk.CTkLabel(self.sidebar, text="Menu", font=ctk.CTkFont(weight="bold")).pack(pady=10, padx=10)

        ctk.CTkButton(self.sidebar, text="Start Page",font=ctk.CTkFont(weight="bold"), fg_color="transparent", command=lambda: self.show_frame("StartPage")).pack(padx=10, pady=10)
        ctk.CTkButton(self.sidebar, text="Scraper Page",font=ctk.CTkFont(weight="bold"), fg_color="transparent", command=lambda: self.show_frame("ScraperPage")).pack(padx=10, pady=10)
        ctk.CTkButton(self.sidebar, text="Classification Page",font=ctk.CTkFont(weight="bold"), fg_color="transparent", command=lambda: self.show_frame("ClassificationPage")).pack(padx=10, pady=10)
        ctk.CTkButton(self.sidebar, text="Result Page", font=ctk.CTkFont(weight="bold"), fg_color="transparent", command=lambda: self.show_frame("ResultPage")).pack(padx=10, pady=10)
        ctk.CTkButton(self.sidebar, text="Analysis Page",font=ctk.CTkFont(weight="bold"), fg_color="transparent", command=lambda: self.show_frame("AnalysisPage")).pack(padx=10, pady=10)
        ctk.CTkButton(self.sidebar, text="Read Me Page",font=ctk.CTkFont(weight="bold"), fg_color="transparent",  command=lambda: self.show_frame("ReadMePage")).pack(padx=10, pady=10)

        container = ctk.CTkFrame(self)
        container.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (StartPage, ScraperPage, ClassificationPage, ResultPage, AnalysisPage, ReadMePage):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("StartPage")
        
        
    def show_frame(self, page_name: str):
        frame = self.frames[page_name]
        frame.tkraise()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
            
        