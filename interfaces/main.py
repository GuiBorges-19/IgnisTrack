import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
import customtkinter
from server_tcp import Server
from relatorios import Relatorios
import queue
import time
import threading
from status_frame import create_status_panel, create_drone_status, add_graphs, update_graph


class Main_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.relatorios = Relatorios(self, controller)
        self.parent = parent
        self.configure(bg="#D9D9D9")
        self.op_fim = False
        
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
        self.body_frame.grid(row=0 , column=0, sticky="nsew", padx=5, pady=5)
        
        self.body_frame.columnconfigure(0, weight=2)  # Coluna do mapa
        self.body_frame.columnconfigure(1, weight=1)  # Coluna do painel de status
        self.body_frame.rowconfigure(0, weight=1)
        
        # frame mapa_frame
        self.map_frame = self.create_map_frame(self.body_frame)
        self.map_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            
        # frame de status_frame
        self.relatorios = Relatorios(self.body_frame, self)
        self.status_frame,self.temp_frame, self.vento_frame, self.hum_frame, self.pressao_frame, operador_entry, area_entry = create_status_panel(self.body_frame, self.controller, self.relatorios.table)
        
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

    #integrar com uma api que transforma a label em si nas coordenadas no mapa (Geocoding API)
        """#barra search do mapa
        search_frame = tk.Frame(self.body_frame)
        search_frame.grid(pady=5)
        
        self.search_entry = tk.Entry(search_frame,width=40)
        self.search_entry.grid(padx=5)
        
        self.search_b = tk.Button(search_frame,text="Pesquisar",command=self.search_local)
        self.search_b.grid(padx=5)"""
        
    """def search_local(self):
        location = self.search_entry.get()
        if location:
            self.map_frame.set_address(location, marker=True)
        else:
            print("Local não encontrado")"""
    
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
        
        global op_ativa
        op_ativa = True
        
        print(f"DEBUG - Tipo de dados_clima: {type(dados_clima)}, Valor: {dados_clima}")  
        
        if hasattr (self, 'op_fim') and self.op_fim:
            pass
        
        if not hasattr(self, 'map_frame'):
            return
        
        if not op_ativa:
            return

        
        if not isinstance(dados_clima,dict):
            print("Erro: Esperado dicionario", type(dados_clima))
            return
        
        if dados_clima:
            add_graphs(dados_clima, self.temp_frame, self.vento_frame, self.hum_frame, self.pressao_frame)
        
        
        if hasattr(self,'drone_marker') and self.drone_marker:
            self.drone_marker.delete()
        self.drone_marker = self.map_frame.set_marker(lat,log,alt)
        
    def check_queue(self):
        ##Função que verifica as coordenadas e atualiza a posiçao do drone
        try:
            while True:
                coordinates = self.coord_queue.get_nowait()
                
                lat,log,altitude = map(float, coordinates.split(','))
                print(f"Coordenadas Processadas: lat={lat}, log = {log}, alt = {altitude}")
                dados_clima = self.server.get_weather(lat,log)##procura o tempo conforme as coordenadas      
                self.update_location(lat,log,altitude,dados_clima)     #atualiza o update_location com a nova posiçao 
        except queue.Empty:
            pass
        self.controller.after(100,self.check_queue)
        
    


    




