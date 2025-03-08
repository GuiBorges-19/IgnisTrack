import socket
import threading
import tkinter as tk
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random



class Server:
    def __init__(self,host = "0.0.0.0", port = 9999, callback = None):
        self.host = host
        self.port = port
        self.callback = callback #atualiza a interface
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.api_key = "16e875e9b38c2081419f66dc2af10bf8"
        
    
    def get_weather(self, lat, log):
            
        #vai buscar os dados metereologicos com base nas coordenadas
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={log}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            temperatura = dados["main"]["temp"]
            humidade = dados["main"]["humidity"]
            pressao = dados["main"]["pressure"]
            vento = dados["wind"]["speed"]
            return {"temperatura": temperatura, "humidade": humidade, "pressao": pressao, "vento": vento}
        else:
            print("Erro a registar os dados climaticos: ", response.status_code)
            return {}

    """def update_ui(labels,lat,log, alt):
        #atualiza a interface com a nova posição e com a metereologia
        labels["Latitude: "].config(text=f"{lat}")
        labels["Longitude: "].config(text=f"{log}")
        labels["Altitude: "].config(text=f"{alt}")"""
        
    def handle_client(self, client_socket):
        #Processa os dados recebidos do "cliente"
        while True:
            data = client_socket.recv(1024)#Lê até 1024 bytes de dados recebidos pelo socket
            if not data:
                break
            try:
                raw_data = data.decode().strip()#tranforma os dados de bytes para string e tira espaços em branco
                print(f"Recebido {raw_data}")
                
                lat,log , alt = map(float,raw_data.split(","))#separa as coordenadas com virgulas e converte para float
                print(f"Posição: Lat:{lat} Log:{log} Alt: {alt}")
                #actual_label(lat, log, alt)
                
                dados_clima = self.get_weather(lat,log)
                
                if self.callback:#atualiza na app
                    self.callback(lat,log,alt,dados_clima)
                     
            except ValueError:
                print(f"Erro a processar coordenaas ",raw_data)
        client_socket.close()
        
    def start_server(self):
        #inicia o servidor para receber as coordenadas do drone
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print("Servidor à escuta em 9999")
        
        while True:
            client_socket, _ = self.server.accept()
            thread = threading.Thread(target = self.handle_client, args = (client_socket,))
            thread.start()
            
    def run(self):
        server_thread = threading.Thread(target=self.start_server, daemon=True)
        server_thread.start()
            
            
            
    
    
    
