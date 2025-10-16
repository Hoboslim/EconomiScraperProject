import customtkinter as ctk
from tkinter import ttk, messagebox
import os
import threading
import subprocess
from Classification.ArticleClassifier import run_classification
from .startPage import StartPage

class ClassificationPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.stop_flag = False

        ctk.CTkLabel(self, text="Classification Page", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        self.articles_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Articles")
        self.csv_dropdown = ttk.Combobox(self, values=self.get_csv_files(), state="readonly")
        if self.get_csv_files():
            self.csv_dropdown.current(0)
        self.csv_dropdown.pack(pady=10)

        ctk.CTkLabel(self, text="Select Ollama Model:").pack(pady=(10, 0))
        self.model_dropdown = ttk.Combobox(self, values=self.get_ollama_models(), state="readonly")
        models = self.get_ollama_models()
        if models:
            self.model_dropdown.current(0)
        self.model_dropdown.pack(pady=5)

        ctk.CTkButton(self, text="Run Classification", command=self.run_selected_classification).pack(pady=10)
        ctk.CTkButton(self, text="Stop Program", fg_color="red", hover_color="#8b0000", command=self.stop_program).pack(pady=10)
        ctk.CTkButton(self, text="Refresh Articles", command=self.refresh_csv_dropdown).pack(pady=5)
        

        self.progress = ctk.CTkProgressBar(self, mode="indeterminate", width=250)
        self.progress.set(0)
        self.progress.pack(pady=10)

    def get_csv_files(self):
        return [f for f in os.listdir(self.articles_folder) if f.endswith(".csv")]

    def refresh_csv_dropdown(self):
        files = self.get_csv_files()
        self.csv_dropdown["values"] = files
        if files:
            self.csv_dropdown.current(0)

    def get_ollama_models(self):
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, encoding="utf-8", timeout=5)
            lines = result.stdout.strip().split("\n")[1:]
            models = [line.split()[0] for line in lines if line.strip()]
            return models or ["gemma3:12b"]
        except Exception as e:
            print(f"Error fetching Ollama models: {e}")
            return ["gemma3:12b"]

    def run_selected_classification(self):
        selected_csv = self.csv_dropdown.get()
        selected_model = self.model_dropdown.get()

        if not selected_csv:
            messagebox.showwarning("No Selection", "Please select a CSV file first.")
            return

        if not selected_model:
            messagebox.showwarning("No Model Selected", "Please select a model first.")
            return

        file_path = os.path.join(self.articles_folder, selected_csv)
        self.stop_flag = False
        self.progress.start()
        threading.Thread(
            target=self._run_classification_task,
            args=(file_path, selected_model),
            daemon=True
        ).start()

    def _run_classification_task(self, file_path, model_name):
        try:
            run_classification(file_path, model_name, stop_flag=lambda: self.stop_flag)
        except Exception as e:
            print(f"Error running classification {e}")
            messagebox.showerror("Error", f"Classification failed: {e}")
        finally:
            self.after(0, self.progress.stop)
            if not self.stop_flag:
                self.after(0, lambda: messagebox.showinfo("Done", "Classification finished!"))
            else:
                self.after(0, lambda: messagebox.showinfo("Stopped", "Classification was stopped."))

    def stop_program(self):
        self.stop_flag = True
        messagebox.showinfo("Stopping", "The program will stop after the current article.")
