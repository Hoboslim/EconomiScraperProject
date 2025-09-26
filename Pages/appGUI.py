import tkinter as tk
from Pages.startPage import StartPage
from Pages.scraperPage import ScraperPage
from Pages.classificationPage import ClassificationPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Webscraper")
        self.geometry("600x500")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, ScraperPage, ClassificationPage):
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
            
        