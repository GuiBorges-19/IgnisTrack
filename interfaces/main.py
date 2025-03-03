import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
import customtkinter
from server_tcp import Server
import queue
from status_frame import create_status_panel, create_drone_status, grafico_temp, grafico_vento, add_graphs


class Main_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.configure(bg="#D9D9D9")
        
        # Configuração do layout principal
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        
        self.drone_labels = {}
        
        self.create_body()
        
        self.drone_marker = None
        self.coord_queue = queue.Queue()
        self.controller.after(100,self.check_queue)
        
        self.server = Server(callback=self.update_location)

    def create_body(self):
        # Cria o corpo da página principal
        self.body_frame = ttk.Frame(self)
        self.body_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.body_frame.columnconfigure(0, weight=2)  # Coluna do mapa
        self.body_frame.columnconfigure(1, weight=1)  # Coluna do painel de status
        self.body_frame.rowconfigure(0, weight=1)
        
        # frame mapa_frame
        self.map_frame = self.create_map_frame(self.body_frame)
        self.map_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.status_frame,self.temp_frame, self.vento_frame = create_status_panel(self.body_frame)
        
        # frame de status_frame
        self.status_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # frame image_frame
        image_frame = tk.Frame(self.status_frame)
        image_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # frame drone_frame
        self.drone_frame, self.drone_labels = create_drone_status(self.body_frame)
        
        # botão "Drone: Ativo" para alternar entre os frames
        for widget in self.status_frame.winfo_children():
            if isinstance(widget, tk.Label) and "Drone: Ativo" in widget.cget("text"):
                widget.bind("<Button-1>", lambda e: self.show_frame(self.drone_frame))

        # botão "Voltar" para alternar entre os frames
        button_2 = self.drone_frame.winfo_children()[-1]
        button_2.configure(command=lambda: self.show_frame(self.status_frame))

        # mostra o frame inicial - frame 1
        self.show_frame(self.status_frame)

    def create_map_frame(self, parent):
        #Cria a área do mapa interativo
        map_frame = TkinterMapView(parent, borderwidth=2, corner_radius=0, width=600, height= 500,relief="solid")
        map_frame.set_tile_server("https://mt0.google.com/vt/lyrs=m&h11=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        
        return map_frame
    
    def show_frame(self, frame):
        self.status_frame.grid_remove()  # Esconde o painel de status
        self.drone_frame.grid_remove()   # Esconde o painel do drone
        frame.grid(row=0, column=1, sticky="nsew")  # Exibe o novo frame
    
    def update_location(self, lat, log ,alt,dados_clima):
        
        print(f"DEBUG - Tipo de dados_clima: {type(dados_clima)}, Valor: {dados_clima}")  # <-- Adicione isto
        
        if not hasattr(self, 'map_frame'):
            return
        
        if not isinstance(dados_clima,dict):
            print("Erro: Esperado dicionario", type(dados_clima))
            return
        
        if self.drone_marker:
            self.drone_marker.delete()
        
        self.drone_marker = self.map_frame.set_marker(lat,log,alt)
        
        if dados_clima:
            add_graphs(dados_clima,self.temp_frame,self.vento_frame)
            
    def check_queue(self):
        try:
            while True:
                coordinates = self.coord_queue.get_nowait()
                
                lat,log,altitude = map(float, coordinates.split(','))
                print(f"Coordenadas Processadas: lat={lat}, log = {log}, alt = {altitude}")
                dados_clima = self.server.get_weather(lat,log)         
                self.update_location(lat,log,altitude,dados_clima)       
        except queue.Empty:
            pass
        self.controller.after(100,self.check_queue)


    




