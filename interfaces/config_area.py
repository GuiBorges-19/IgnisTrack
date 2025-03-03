import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import subprocess

class Config_area(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        self.create_body()
     
    def create_body(self):
        #Cria o corpo da página principal.
        self.body_frame = ttk.Frame(self)
        self.body_frame.grid(row = 0, column=0, sticky="nseww", padx=10,pady=10)
        
        self.body_frame.columnconfigure(0, weight=2) #coluna do mapa
        self.body_frame.columnconfigure(1, weight=1) #coluna do painel de status
        self.body_frame.rowconfigure(0, weight=1)    

         #Cria o framme de apresentação do mapa
        map_frame = self.create_map_frame(self.body_frame)
        map_frame.grid(row=0, column=0, sticky="nsew", padx=10,pady=10) 
        
        status_frame = self.create_status_panel(self.body_frame)
        status_frame.grid(row = 0, column=1, sticky="nseww", padx=10,pady=10)
        
    # Função que apresenta o mapa no mape_frame
    def create_map_frame(self, parent):
         #Cria a área do mapa interativo
        map_frame = ttk.Frame(parent, borderwidth=2, relief="solid")
        map_label = tk.Label(
            map_frame,
            text="Mapa Interativo",
            font=("Arial", 14),
            bg="#e0e0e0",
            fg="#333",
            width=50,
            height=20,
        )
        map_label.pack(fill="both", expand=True, padx=10, pady=10)
        return map_frame
    
    #Função que apresenta toda a informação do status_frame
    def create_status_panel(self, parent):
        """Cria o painel de status do sistema."""
        
        #Criação da Frame do Status
        status_frame = ttk.Frame(parent, borderwidth=2, relief="solid", padding=10)
  
        #Label e Entry de apresentação da área configurada
        area_label = ttk.Label(status_frame, text="Nome da Área:", font=("Inter", 14))
        area_label.grid(row=1, column=0, sticky="w", pady=5)
        area_entry = ttk.Entry(status_frame)
        area_entry.grid(row=1, column=1, sticky="ew", pady=5)
        
        #Configura o layout do frame de status
        status_frame.columnconfigure(1, weight=1)
        
        return status_frame
    
 
        
    