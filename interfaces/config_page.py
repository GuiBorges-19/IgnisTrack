import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class Config(tk.Frame): 
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="nsew")
        
        # Carregar e armazenar a imagem como atributo da classe
        logo = Image.open("figures/tools.png").resize((320,320), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(logo)  
        
        logo_label = ttk.Label(header_frame, image= self.logo_img, background="#2E5984")
        logo_label.grid(row=0, column=0, columnspan=5, padx=600, pady=5, sticky="ew")
    
        
