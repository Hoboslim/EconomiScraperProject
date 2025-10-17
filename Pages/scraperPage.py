import customtkinter as ctk
from tkinter import messagebox
import os
import threading
import importlib.util

class ScraperPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.stop_flag = False

        ctk.CTkLabel(self, text="Scraper Page", font=("Arial", 18, "bold")).pack(pady=20)

        self.folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Scrapers")

        
        scraper_files = [fname for fname in os.listdir(self.folder) if fname.endswith(".py")]

       
        self.scraper_map = {
            fname.replace("Scraper", "").replace(".py", ""): fname
            for fname in scraper_files
        }

        display_names = list(self.scraper_map.keys())

        self.dropdown_var = ctk.StringVar()
        self.dropdown = ctk.CTkOptionMenu(self, values=display_names, variable=self.dropdown_var)
        if display_names:
            self.dropdown_var.set(display_names[0])
        self.dropdown.pack(pady=10)

        ctk.CTkButton(self, text="Run Scraper", command=self.run_scraper).pack(pady=10)
        ctk.CTkButton(self, text="Stop Scraper", fg_color="red", hover_color="#8b0000",
                      command=self.stop_scraper).pack(pady=10)

        self.progress = ctk.CTkProgressBar(self, mode="indeterminate", width=250)
        self.progress.set(0)
        self.progress.pack(pady=10)

    def run_scraper(self):
        selected_display = self.dropdown.get()
        if not selected_display:
            messagebox.showwarning("No Selection", "Please select a scraper first.")
            return

        
        selected_scraper = self.scraper_map[selected_display]
        filepath = os.path.join(self.folder, selected_scraper)

        self.stop_flag = False
        self.progress.start()

        threading.Thread(target=self._run_scraper_task, args=(filepath,), daemon=True).start()

    def _run_scraper_task(self, filepath):
        try:
            module_name = os.path.splitext(os.path.basename(filepath))[0]
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "run_scraper"):
                module.run_scraper(stop_flag=lambda: self.stop_flag)
            else:
                raise AttributeError(f"Module '{module_name}' has no run_scraper(stop_flag) function")

        except Exception as e:
            err_msg = str(e)
            self.after(0, lambda err=err_msg: messagebox.showerror("Error", f"Scraper failed: {err}"))

        finally:
            self.after(0, self.progress.stop)
            if not self.stop_flag:
                self.after(0, lambda: messagebox.showinfo("Done", "Scraper finished!"))
            else:
                self.after(0, lambda: messagebox.showinfo("Stopped", "Scraper was stopped."))

    def stop_scraper(self):
        if not self.stop_flag:
            self.stop_flag = True
            messagebox.showinfo("Stopping", "Scraper will stop shortly...")
