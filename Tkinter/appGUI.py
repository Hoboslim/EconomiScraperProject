import tkinter as tk
from tkinter import ttk
import os
import subprocess

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
folder = os.path.join(root_dir, "Scrapers")

#folder = "Scrapers"
options = [fname for fname in os.listdir(folder) if fname.endswith(".py")]

def run_scraper():
    selected_scraper = dropdown.get()
    if selected_scraper:
        filepath = os.path.join(folder, selected_scraper)
        try:
            subprocess.run(["python", filepath], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running this file: {e}")


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

run_btn = tk.Button(root,text="Run scraper", command=run_scraper)
run_btn.pack(padx=10, pady=10)

root.mainloop()