import customtkinter as ctk
from .startPage import StartPage
from .scraperPage import ScraperPage
from .classificationPage import ClassificationPage
from .resultPage import ResultPage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("Webscraper")
        self.geometry("600x500")
        self.minsize(600, 500)
        
        
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, ScraperPage, ClassificationPage, ResultPage):
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
            
        