import tkinter as tk
from tkinter import ttk
import os

folder = "Scrapers"
options = [fname for fname in os.listdir(folder) if fname.endswith(".py")]

root = tk.Tk()
root.title("Webscraper")
root.geometry("500x500")

label1 = tk.Label(root, text="Välkommen till webscraper!", font=("Arial", 18, "bold"))
label1.pack(padx=20, pady=20)

label2 = tk.Label(root, text="Välj en webbsida: ", font=("Arial", 15))
label2.pack(padx=10, pady=10)

dropdown = ttk.Combobox(root, values=options, state="readonly")
dropdown.current(0)
dropdown.pack(pady=10)

root.mainloop()