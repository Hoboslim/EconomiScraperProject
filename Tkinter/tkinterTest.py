import tkinter as tk
from tkinter import ttk


def choose_scraper(event=None):
    choice = combo.get()
    label.config(text=f"Du valde: {choice}", font=("Arial", 12))
    
    if choice == "Aftonbladet":
         print("Processing..")

    elif choice == "Expressen":
        print("Processing..")

    elif choice == "Dagens Industri":
         print("Processing..")


root = tk.Tk()
root.title("Webscraper")
root.geometry("500x500")

label1 = tk.Label(root, text="Välkommen till webscraper!", font=("Arial", 18, "bold"))
label1.pack(padx=20, pady=20)

label2 = tk.Label(root, text="Välj en webbsida: ", font=("Arial", 15))
label2.pack(padx=10, pady=10)

options = ["Aftonbladet", "Expressen", "Dagens Industri"]
combo = ttk.Combobox(root, values=options, state="readonly")
combo.current(0)
combo.pack(pady=10)

combo.bind("<<ComboboxSelected>>", choose_scraper)

label = tk.Label(root, text="")
label.pack(pady=10)



root.mainloop()