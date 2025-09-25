import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, root_dir)

from Classification.ArticleClassifier import run_classification

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess

folder = os.path.join(root_dir, "Scrapers")
articles = os.path.join(root_dir, "Articles")


#folder = "Scrapers"
options = [fname for fname in os.listdir(folder) if fname.endswith(".py")]



def get_csv_files():
    return [f for f in os.listdir(articles) if f.endswith(".csv")]

def run_scraper():
    selected_scraper = dropdown.get()
    if selected_scraper:
        filepath = os.path.join(folder, selected_scraper)
        try:
            subprocess.run(["python", filepath], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running this file: {e}")


def exit_program():
    if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
        root.destroy()
 
    
def choose_file():

    initial_directory = os.path.join(os.path.dirname(__file__), "../Articles")

    file_path = filedialog.askopenfilename(
        initialdir = initial_directory,
        title = "Välj CSV-fil",
        filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
    )

def run_selected_classification():
    selected_csv = csv_dropdown.get()
    if selected_csv:
        file_path = os.path.join(articles, selected_csv)
        run_classification(file_path)



root = tk.Tk()
root.title("Webscraper")
root.geometry("500x500")

#Meny
menubar = tk.Menu(root)
file = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Menu", menu=file)
file.add_command(label="Scraper", command=None)
file.add_command(label="Classification", command=None)
file.add_command(label="Diagram", command=None)
file.add_separator()
file.add_command(label="Exit", command=exit_program)
root.config(menu=menubar)


label1 = tk.Label(root, text="Välkommen till webscraper!", font=("Arial", 18, "bold"))
label1.pack(padx=20, pady=20)

label2 = tk.Label(root, text="Välj en webbsida: ", font=("Arial", 15))
label2.pack(padx=10, pady=10)

dropdown = ttk.Combobox(root, values=options, state="readonly")
dropdown.current(0)
dropdown.pack(pady=10)

run_scraper_btn = tk.Button(root,text="Run Scraper", command=run_scraper)
run_scraper_btn.pack(padx=10, pady=10)

label3 = tk.Label(root, text="Välj en fil för klassifikation:  ", font=("Arial", 15))
label3.pack(padx=10, pady=10)

csv_dropdown = ttk.Combobox(root, values=get_csv_files(), state="readonly")
if get_csv_files():
    csv_dropdown.current(0)
csv_dropdown.pack(pady=10)

run_classification_btn = tk.Button(root, text="Run Classification", font=("Arial", 15), command=run_selected_classification)
run_classification_btn.pack(padx=10, pady=10)

root.mainloop()