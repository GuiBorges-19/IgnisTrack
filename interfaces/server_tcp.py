import socket
import threading
import tkinter as tk
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from functools import partial
import mysql.connector
import queue



class Server:
    #endereço ip onde o servidor escuta, port de escuta, func para atualizar drone e informaçoes, callback para atuualizar os dados das operaçao na bd
    def __init__(self,host = "0.0.0.0", port = 9999, callback = None, callback_1 = None):
        self.host = host
        self.port = port
        self.callback = callback #atualiza a interface
        self.callback_1 = callback_1
        
        #criação do server socket (tcp-ip)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #CHAVE DE CAPI TEMPO    
        self.api_key = "16e875e9b38c2081419f66dc2af10bf8"
        
        self.first_lat = None   
        self.first_log = None
        self.first_alt = None
        self.first_coord = False
        
        self.marca = None   
        self.modelo = None
        self.autonomia = None


    def set_callbacks(self, callback=None, callback_1=None, callback_video = None):
        # Método para configurar os callbacks
        self.callback = callback
        self.callback_1 = callback_1
        self.callback_video = callback_video
       
        
    def start_server(self):
        
        try:
            #inicia o servidor para receber as coordenadas do drone
            
            #ligar ao port e host
            self.server.bind((self.host, self.port))
            
            #pode ouvvir ate 5 conexoes
            self.server.listen(5)
            print("Servidor à escuta em 9999")
            
            while True:
                try:
                    #endereço no pc aceite
                    client_socket,addr = self.server.accept()
                    print(f"Conexao recebida de {addr}")

                    ##cria uma thread para lidar com o lciente
                    thread = threading.Thread(target = self.handle_client, args = (client_socket,), daemon=True)
                    thread.start()
                    
                except socket.timeout:
                    continue
        except OSError as e:
            print(f"Erro ao iniciar o servidor: {e}")
    
    def handle_client(self, client_socket):
        #Processa os dados recebidos do "cliente"
        
        while True:
            try:
                data = client_socket.recv(1024).decode().strip()  # Lê até 1024 bytes de dados recebidos pelo socket
                if not data:
                    break
                
                try:
                    lat,log , alt, marca, modelo, autonomia= data.split(",")#separa as coordenadas com virgulas e converte para float
                    
                    lat,log , alt = map(float,[lat,log,alt] )
                    
                    marca, modelo, autonomia = str(marca), str(modelo), str(autonomia)
                    
                    self.marca = marca   
                    self.modelo = modelo
                    self.autonomia = autonomia
                    
                    print(f"Posição: Lat:{lat} Log:{log} Alt: {alt}")
                    print(f"Drone: Marca;{marca}, Modelo: {modelo}, Autonomia :{autonomia}")
                    
                    dados_clima = self.get_weather(lat,log)
                    
                    if self.first_coord == False:
                        self.set_first_coordinates(lat,log,alt)
                        
                    if self.callback is not None:
                        self.callback(lat, log, alt, dados_clima, marca, modelo,autonomia)
                            
                    if self.callback_1:
                        self.callback_1(lat, log, alt)

                except ValueError:
                    print(f"Erro a processar coordenadas ",data)
                    
            except ConnectionResetError:
                break
        client_socket.close()    
            
            
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
            print(f"Temperatura: {temperatura}°C, Humidade: {humidade}%, Pressão: {pressao} hPa, Vento: {vento} m/s")

            return {"temperatura": temperatura, "humidade": humidade, "pressao": pressao, "vento": vento}
        else:
            print(f"Erro a registar os dados climaticos:{response.text} ")
            return {}

        
    def set_first_coordinates(self,lat, log, alt):
        if not self.first_coord:
            self.first_lat = lat
            self.first_log = log
            self.first_alt = alt
            self.first_coord = True
                
            print(f"aaaaaa{self.first_lat, self.first_log,self.first_alt}")
            self.save_coordinates(self.first_lat, self.first_log,self.first_alt)
    
    def save_coordinates(self,lat,log,alt):
        conexao = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='guilherme',
            database='drone_project'
        )
        cursor = conexao.cursor(buffered=True)
        
        cursor.execute("INSERT INTO CoordenadasOperacao (latitude, longitude, altitude) VALUES (%s, %s, %s)",
                       (self.first_lat, self.first_log, self.first_alt))
        self.coordenadas_id = cursor.lastrowid
        
        cursor.execute("INSERT INTO drone (modelo, marca, autonomia) VALUES (%s, %s, %s)", (self.modelo, self.marca, self.autonomia))

        self.drone_id = cursor.lastrowid

        
        conexao.commit()
        cursor.close()
        conexao.close()
        
    def stop_server(self):
        self.op_ativo = False
        try:
            
            fake_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            fake_socket.connect((self.host, self.port))
            fake_socket.close()
        except OSError:
            pass  
        
        self.server.close()  #
        
    def run(self):
        server_thread = threading.Thread(target=self.start_server, daemon=True)
        server_thread.start()    
        
 
            
            
            
    
    
    
