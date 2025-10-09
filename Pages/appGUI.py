import customtkinter as ctk
from tkinter import Menu
from .startPage import StartPage
from .scraperPage import ScraperPage
from .classificationPage import ClassificationPage
from .resultPage import ResultPage
from .analysisPage import AnalysisPage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("Webscraper")
        self.geometry("600x500")
        self.minsize(600, 500)
        
        menubar = Menu(self)
        self.config(menu=menubar)
        
        pages_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Pages", menu=pages_menu)
        
        pages_menu.add_command(label="Start Page", command=lambda: self.show_frame("StartPage"))
        pages_menu.add_command(label="Scraper Page", command=lambda: self.show_frame("ScraperPage"))
        pages_menu.add_command(label="Classification Page", command=lambda: self.show_frame("ClassificationPage"))
        pages_menu.add_command(label="Result Page", command=lambda: self.show_frame("ResultPage"))
        pages_menu.add_command(label="Analysis Page", command=lambda: self.show_frame("AnalysisPage"))
        
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, ScraperPage, ClassificationPage, ResultPage, AnalysisPage):
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
            
        