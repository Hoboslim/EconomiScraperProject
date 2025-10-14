import customtkinter as ctk

class ReadMePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)


        ctk.CTkLabel(self, text="Read Me Page", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20, padx=20)
        ctk.CTkButton(self, text="Read Instructions", command=self.show_instructions).pack(pady=10)
        self.textbox1 = ctk.CTkTextbox(self, width=600, height=300)

        ctk.CTkButton(self, text="Read ME", command=self.show_readme).pack(pady=10)
        self.textbox2 = ctk.CTkTextbox(self, width=600, height=200)
        ctk.CTkButton(self, text="Back to Home", command=lambda: controller.show_frame("StartPage")).pack(side="bottom", pady=10)

    def show_instructions(self):
        self.textbox1.pack(pady=10)
        
        with open("texts/Instructions.txt", "r", encoding="utf-8") as f:
            instructions_text = f.read()
            
        self.textbox1.insert("0.0", instructions_text)
        self.textbox1.configure(state="disabled")

     
    def show_readme(self):
        self.textbox2.pack(pady=10)
        
        with open("texts/README.txt", "r", encoding="utf-8") as f:
            readme_text = f.read()
            
        self.textbox2.insert("0.0", readme_text)
        self.textbox2.configure(state="disabled")
      
    

    
            


        
       

            



