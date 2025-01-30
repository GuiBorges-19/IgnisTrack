import tkinter as tk
from tkinter import ttk

class Config(tk.Frame): 
    def __init__(self, parent, controller):
        super().__init__(parent)
      
        self.controller = controller
        label = ttk.Label(self, text="Página de Configurações", font=("Arial", 18))
        label.pack(pady=20)
        
      
   