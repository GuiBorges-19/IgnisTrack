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
        """Cria a área do mapa interativo."""
        map_frame = ttk.Frame(parent, borderwidth=2, relief="solid")
        map_label = tk.Label(
            map_frame,
            text="Mapa Interativo (Placeholder)",
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

        #Label e Entry de apresentação do Operador
        operador_label = ttk.Label(status_frame, text="Operador:", font=("Inter", 14))
        operador_label.grid(row=0, column=0, sticky="w", pady=5)
        self.operador_entry = ttk.Entry(status_frame)
        self.operador_entry.grid(row=0, column=1, sticky="ew", pady=5)
  
        #Label e Entry de apresentação da área configurada
        area_label = ttk.Label(status_frame, text="Área:", font=("Inter", 14))
        area_label.grid(row=1, column=0, sticky="w", pady=5)
        area_entry = ttk.Entry(status_frame)
        area_entry.grid(row=1, column=1, sticky="ew", pady=5)
        
        #Configura o layout do frame de status
        status_frame.columnconfigure(1, weight=1)
        
        def open_drone():
            os.system("drone.py")
        
        
        drone_status = tk.Label(
            status_frame,
            text="Drone: Ativo",
            font=("Inter", 14),
            fg="green",
            cursor="hand2"
        )
        
        drone_status.bind("<Button-1>", lambda e: open_drone())
        
        # Adiciona scroll frame e scrollbar no status_frame
        self.scroll_canvas = tk.Canvas(status_frame, height=650)
        self.scroll_canvas.grid(row=3 ,column=0, sticky="nsew",columnspan=2, pady=10)
        
        #Criação do scrollbar vertical
        self.scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.scroll_canvas.yview)
        self.scrollbar.grid(row=3 ,column=2, sticky="nsew")
        
        #Configuração do canvas para usar o scroll
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        #Frame dos graficos dentro de status_frame
        self.graph_frame = ttk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0,0), window=self.graph_frame, anchor="nw")
        
        #ajusta a rolagem do scroll
        self.graph_frame.bind(
            "<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")) # semmpre que sao adicionados graficos sao mostrados todos
        )
        
           #adiciona os graficos ao frame
        self.add_graphs()
        return status_frame
    
    def add_graphs(self):
        # Adicionar gráficos ao frame
        for i in range(5):
            grafico = self.criar_grafico()
            grafico_canvas = FigureCanvasTkAgg(grafico, master=self.graph_frame)
            grafico_canvas.get_tk_widget().pack(pady=10)

        
    def criar_grafico(self):
        fig, ax = plt.subplots(figsize=(4, 3))  # Define o tamanho do gráfico
        ax.plot([0, 1, 2, 3, 4], [0, 1, 4, 9, 16])  # Plotando um gráfico simples
        ax.set_title("Exemplo de Gráfico")
        return fig
    
        
    