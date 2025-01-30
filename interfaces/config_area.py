import tkinter as tk
from tkinter import ttk


class Config_area(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f5f5f5")
    

        label = ttk.Label(self, text="Página de Configuraçao da area", font=("Arial", 18))
        label.pack(pady=20)
        

       