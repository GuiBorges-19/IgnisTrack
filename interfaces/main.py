import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkbootstrap.scrolled import ScrolledFrame 
from tkintermapview import TkinterMapView
import customtkinter
from interfaces.relatorios import Relatorios
import math
from geopy.distance import geodesic
from PIL import Image, ImageTk
import queue
import requests
from ttkbootstrap.style import Style
import time
from interfaces.server_tcp import Server
import polyline
from interfaces.status_frame import create_status_panel, create_drone_status, add_graphs


class Main_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        
        #relção com a pagina principal
        self.parent = parent
    
        self.configure(bg="#D9D9D9")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Configuração do layout principal
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
       
        self.drone_labels = {}

        self.drone_marker = None
        self.relatorios = Relatorios(self, controller)
        
        self.local_marker_icon = Image.open("figures/fire.png").resize((30, 30))
        self.local_marker_icon = ImageTk.PhotoImage(self.local_marker_icon)
        
        self.drone_marker_icon = Image.open("figures/drone.png").resize((30, 30))
        self.drone_marker_icon = ImageTk.PhotoImage(self.drone_marker_icon)
        
        
        #guarda os pontos de risco conforme as coordenadas
        self.plaves_cash = []
        
        #pontos pesquisados na barra de pesquisa guardados em vetores
        self.pontos_pesquisados = []
        
        #criar a interface
        self.create_body()
        
        #3Instancia do servidor para comunicar com o mesmo
        self.server = Server()
        
        #Chamada para abrir o servidor 
        self.setup_callbacks()
        
    
        
    def create_body(self):
        # Cria o corpo da página principal
        style = Style()
        style.configure("Custo.TFrame", background ="#D9D9D9" )
        
        self.body_frame = ttk.Frame(self, borderwidth=2, style="Custo.TFrame")
        self.body_frame.grid(row=0 , column=0, sticky="nsew", padx=30, pady=5)

        self.body_frame.columnconfigure(0, weight=4)  # Coluna do mapa
        self.body_frame.columnconfigure(1, weight=2)  # Coluna do painel de status
        self.body_frame.rowconfigure(0, weight=1)
        
        # frame mapa_frame
        self.map_frame = self.create_map_frame(self.body_frame)
        self.map_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=30)
            
        # frame de status_frame        
        self.status_frame,self.temp_frame, self.vento_frame, self.hum_frame, self.pressao_frame, self.operador_entry, self.area_entry = create_status_panel(self.body_frame, self.controller, self.relatorios.table)
        
        self.status_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=30)
        

        # frame drone_frame
        self.drone_frame, self.drone_labels, self.atualizar_labels, self.atualizar_drone = create_drone_status(self.body_frame)
        
         # Criação do painel lateral dentro do mapa
        self.info_panel = ScrolledFrame(self.map_frame,width=250, height=100)
        self.info_panel.grid_propagate(False)  # Impede o redimensionamento do painel
        self.info_panel.place(relx=0.0, rely=1.0, anchor="sw")
         
        self.info_title = tk.Label(self.info_panel, text="Informações", fg="black", bg="#FFFFFF")
        self.info_title.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    
        # botão "Drone: Ativo" para alternar entre os frames
        for widget in self.status_frame.winfo_children():
            if isinstance(widget, tk.Label) and "Drone: Ativo" in widget.cget("text"):
                widget.bind("<Button-1>", lambda e: self.show_frame(self.drone_frame))

        # botão "Voltar" para alternar entre os frames
        button_2 = self.drone_frame.winfo_children()[-1]
        button_2.configure(command=lambda: self.show_frame(self.status_frame))

        #frame da barra de pesquisa, com definição da label, entry e button
        search_frame = ttk.Frame(self.map_frame, style="Custo.TFrame")
        search_frame.place(relx=0.5, rely=0.01, anchor="n")  # Centraliza no topo do mapa

        search_label = ttk.Label(search_frame, text="Pesquisar Localização:", background="#D9D9D9", font=("Helvetica", 10, "bold"))
        search_label.grid(row=0, column=0, padx=(0, 5), pady=5)

        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5)


        #Ao clicar no butao chama a funçao search_local
        self.search_b = ttk.Button(search_frame, text="Pesquisar", command=self.search_local, style="success.TButton")
        self.search_b.grid(row=0, column=2, padx=5)

    #Chamada quando se clica no butão pesquisar, faz o caminho por estrada entre locais
    def search_local(self):
        location = self.search_entry.get().strip().lower()
        
        #3Se existir drone, ele usa drone como referencia e faz um caminho desde um local até ao drone
        if location == "drone":
            # Verificar se há uma posição conhecida do drone
            if hasattr(self, 'drone_marker') and self.drone_marker is not None:
                drone_lat, drone_lon = self.drone_marker.position  # Obtém a posição do drone
                # Adiciona a posição do drone como ponto pesquisado
                self.pontos_pesquisados.append((drone_lat, drone_lon))
                
                # Verificar se há um ponto anterior para calcular a distância
                if len(self.pontos_pesquisados) >= 2:
                    lat1, lon1 = self.pontos_pesquisados[-2]  # Último ponto pesquisado antes do drone
                    lat2, lon2 = self.pontos_pesquisados[-1]  # Posição do drone
                    
                    # Calcular distância e tempo por estrada
                    distancia, tempo = self.get_distance_estrada(lat1, lon1, lat2, lon2)
                    
                    # Traçar o caminho no mapa
                    path_points = self.get_diretions(lat1, lon1, lat2, lon2)
                    if path_points:
                        self.map_frame.set_path(path_points)
                    
                    # Exibir distância e tempo no mapa
                    if distancia and tempo:
                        lat_meio = (lat1 + lat2) / 2
                        lon_meio = (lon1 + lon2) / 2
                        self.map_frame.set_marker(lat_meio, lon_meio, text=f"{distancia} {tempo}")
                        print(f"Distância por estrada: {distancia}, Tempo estimado: {tempo}")
                    else:
                        print("Não foi possível calcular a distância por estrada.")
                else:
                    # Se não há ponto anterior, apenas marcar a posição do drone
                    self.map_frame.set_position(drone_lat, drone_lon)
                    print("Posição do drone marcada. Pesquise outro ponto para calcular a distância.")
            else:
                messagebox.showerror("Erro", "Nenhuma posição do drone disponível.")
        elif location:
            # Pesquisa normal para outros locais, sem ser com o drone
            self.get_coordinates(location)
        else:
            messagebox.showerror("Erro", "Nenhum local inserido.")
    
    
    def get_coordinates(self, location):
        api_key = "AIzaSyC7qzg5Ug4H5h1fbxsrr42n4U5hiq6APe0"
        
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            #Verifica se a api encontrou o local e extrai os dados do local
            if data["status"] == "OK":
                latitude = data["results"][0]["geometry"]["location"]["lat"]
                longitude = data["results"][0]["geometry"]["location"]["lng"]
            
                ##Atualiza o mapa
                self.map_frame.set_marker(latitude,longitude)
                self.map_frame.set_position(latitude,longitude)
                
                #guarda o ponto pesquisado no vetor
                self.pontos_pesquisados.append((latitude,longitude))
                
                #Se houver dois pontos, faz a rota por estrada entre eles
                if len(self.pontos_pesquisados) >=2:
                    lat1,log1 = self.pontos_pesquisados[0]
                    lat2,log2 = self.pontos_pesquisados[-1]
                    distancia, tempo = self.get_distance_estrada(lat1,log1,lat2,log2)
                    
                    #vai buscar o caminho e faz no mapa
                    path_points = self.get_diretions(lat1,log1,lat2,log2)
                    if path_points:
                        self.map_frame.set_path(path_points)
                    
                    if distancia and tempo:
                        print(f"Distância por estrada: {distancia}, Tempo estimado: {tempo}")
                    else:
                        print("Não foi possível calcular a distância por estrada.")
                
            else:
                messagebox.showerror("Erro", "Local não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao procurar local: {e}")
            
    #calcular a distancia e o tempo de viagem por estrada entre dois locais
    def get_distance_estrada(self,lat1,log1,lat2,log2):
        api_key = "AIzaSyAZECjA2gMnQQREoDWjr4udXib69vh1DJQ"
        
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json"
        
        
        #Define os parametros necessarios
        origins = f"{lat1},{log1}"
        destination = f"{lat2},{log2}"
        
        params = {"origins": origins,
                  "destinations": destination,
                  "key": api_key,
                  "mode": "driving",}
        response = requests.get(url,params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                elemento = data['rows'][0]['elements'][0]
                distancia = elemento['distance']['text']
                tempo = elemento['duration']['text']
                
                #faz o ponto medio para inserir o marker com o tempo e distancia no meio
                lat_meio = (lat1 + lat2) / 2
                log_meio = (log1 + log2) / 2

                self.map_frame.set_marker(lat_meio, log_meio, text=f"{distancia} {tempo}")
                
                return distancia, tempo
            else:
                print(f"Erro na API: {data['status']}")
                return None, None
        else:
            print(f"Erro: {response.text}")
            return None, None
        
    #Função que obtem o caminho entre os dois locais
    def get_diretions(self, lat1,log1,lat2,log2):
        
        api_key = "AIzaSyAZECjA2gMnQQREoDWjr4udXib69vh1DJQ"
        
        url = f"https://maps.googleapis.com/maps/api/directions/json"
        
        #Define a origem e o destino
        origin = f"{lat1},{log1}"
        destination = f"{lat2},{log2}"
        
        params = {"origin": origin,
                  "destination": destination,
                  "key": api_key,
                  "mode": "driving",}
        response = requests.get(url,params=params)
        
        ##processa a resposta e retorna o caminho
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                route = data["routes"][0]
                poly_line = route["overview_polyline"]["points"]
                path_points = polyline.decode(poly_line)
                return path_points
            else:
                print("Erro na rota: ",data["status"])
        else:
            print("Erro")
            
        return []
            
    #Função que retorna os locais de risco conforme a posição do drone em volta de 1000 mtros
    def get_risc_places(self, lat,lon,radius = 1000):
        api_key = "AIzaSyC7qzg5Ug4H5h1fbxsrr42n4U5hiq6APe0"
        
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius={radius}&key={api_key}"

        try:
            #envia a requisição
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200 and data["status"] == "OK":
                
                #resultados encontrados
                places = data["results"]
                for place in places:
                    #para cada local extrai o nome e o endereço(se possivel)
                    name = place["name"]
                    address = place.get("vicinity", "Endereço não encontrado")
                    print(f"Ponto de Interesse: {name}, Endereço:{address}")
                    return places
                    
                else:
                    print(f"Erro ao encontrar lugares: {data.get('status')}")
                    
                    return []
        except Exception as e:
            print(f"Erro:{e}")
            return []
            
    def display_places_on_canvas(self, places, lat, lon):
        map_widget = self.map_frame
        
        #lista para os markers
        markers = []

        #3distancia de segurança
        distancia_critica = 100

        #linha do grid do painel lateral
        row = 1

        #percorre os pontos de interesse
        for place in places:
           
            if 'name' in place:
                name = place["name"]
            else:
                name = "Nome não disponível"   

            address = place.get("vicinity", "Endereço não encontrado")
            place_lat = place["geometry"]["location"]["lat"]
            place_lon = place["geometry"]["location"]["lng"]

            #calculo da distancia entre o drone e o local
            drone_position = (lat, lon)
            place_position = (place_lat, place_lon)
            distance = geodesic(drone_position, place_position).meters
            distance_text = f" {distance:.2f} metros"

            print(f"Ponto de Interesse Nome: {name}, Endereço: {address}, Distância: {distance_text}")

            # Exibir a distância no painel de informações
            poi_label = tk.Label(self.info_panel, text=f"{name} = {distance:.1f}",  bg="#FFFFFF")
            poi_label.grid(row=row, column=0, sticky="w", padx=5)
            row += 1

            # Colocar marcador no mapa
            marker = map_widget.set_marker(place_lat, place_lon, text=name, icon=self.local_marker_icon)
            markers.append({'marker': marker, 'place': place, 'distance': distance_text})

        # Atualizar os pontos de interesse em tempo real
        self.update_poi(markers, lat, lon)


    def update_poi(self, places, lat, lon):
        #verifica se os dados mudaram
        current_data = (places, round(lat,6), round(lon,6))
        
        if current_data == self.last_poi:
            return #dados iguais nao atualiza interface
        
        self.last_poi = current_data
        
        # Limpar o painel atual antes de adicionar os novos dados
        for widget in self.info_panel.winfo_children():
            widget.destroy()

        row = 1  # Iniciar a contagem das linhas 

        # Para cada lugar calcular a distância e atualizar a label
        for place in places:
            name = place['place']['name']
            place_lat = place['place']["geometry"]["location"]["lat"]
            place_lon = place['place']["geometry"]["location"]["lng"]

            # Calcular a distância do drone até o POI
            drone_position = (lat, lon)
            place_position = (place_lat, place_lon)
            distance = geodesic(drone_position, place_position).meters
            distance_text = f"{name}: {distance:.2f} metros"


            # Atualizar o painel lateral
            distance_label = tk.Label(self.info_panel, text=distance_text, fg="#FF0000", bg="#FFFFFF")
            distance_label.grid(row=row, column=0, sticky="w", padx=5)
            row += 1  # Avançar para a próxima linha
            
    #Função que calcula o indece de probabilidade de incendio
    def get_fwi(self,lat,log):
        
        self.dados = self.server.get_weather(lat,log)
        
        temperature = self.dados.get("temperatura")
        humidity = self.dados.get("humidade")
        vento = self.dados.get("vento")
        
        
        
        fwi = (temperature * vento) / (humidity + 1)  
        return fwi
        
    ##Função que classifica  o indice de probabilidade de incendio
    def fwi_classification(self,fwi):
        
        if fwi is None:
            return "Desconhecido", "grey"
        elif fwi < 5:
            return "Baixo","green"
        elif fwi < 15:
            return "Moderado","yellow"
        elif fwi < 30:
            return "Elevado","orange"
        else:
            return "Extremo", "red"
        
    #Função que cria o grafico cicular do FWI
    def canvas_fwi(self,lat,log):
        fwi = self.get_fwi(lat,log)
        nivel,cor = self.fwi_classification(fwi)
        
        if hasattr(self, 'gauge_canvas') and self.gauge_canvas.winfo_exists():
            self.gauge_canvas.destroy()
        
        self.gauge_canvas = tk.Canvas(self.map_frame,width=140, height=140,bg="#ffffff",highlightthickness=0)
        self.gauge_canvas.place(relx=1,rely=1,anchor="se", x = 20, y = 20)
        
        self.gauge_canvas.create_oval(20,20,120,120, fill="#eee", outline="#ccc")
        self.gauge_canvas.create_arc(20,20,120,120, start = 0, extent = 270, style = "arc",outline = cor, width = 15)
        
        self.gauge_canvas.create_text(70, 70, text=nivel, fill=cor, font=("Helvetica", 10, "bold"))
        self.gauge_canvas.create_text(70, 95, text=f"FWI: {fwi:.1f}" if fwi else "Sem dados", font=("Helvetica", 8))
        
                        
    def create_map_frame(self, parent):
        #Cria a área do mapa interativo
        map_frame = TkinterMapView(parent, borderwidth=2, corner_radius=0, width=600, height= 500,relief="solid")
        map_frame.set_tile_server("https://mt0.google.com/vt/lyrs=m&h11=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        
        return map_frame
    
    def show_frame(self, frame):
        self.status_frame.grid_remove()  # Esconde o painel de status
        self.drone_frame.grid_remove()   # Esconde o painel do drone
        frame.grid(row=0, column=1, sticky="nsew")  # Exibe o novo frame
        
    def setup_callbacks(self):
    # Função que define os callback
        self.server.set_callbacks(
        callback=self.update_drone_status,
        callback_1=self.server.set_first_coordinates)
        
        self.server.run()
        
    #Função que atualiza a posição do drone, os dados climaticos, painel lateral e o marcador do drone no mapa
    def update_drone_status(self, lat, log, alt,drone_status,marca,modelo,autonomia):
    
        #3Chama update location para atualizar a posição do drone 
        self.after(0, lambda: self.update_location(lat, log, alt,drone_status,marca,modelo,autonomia))
        
       #Pesquisa lugares de risco que estao na lista cache
        if not self.plaves_cash: 
            places = self.get_risc_places(lat,log,1000)#se nao houver, chama função que pesquisa esses lugares
            if places:
                self.plaves_cash = places
                self.after(0, lambda p = places: self.display_places_on_canvas(p,lat,log))#3se ja existirem esses lugares, mostra os lugares no mapa
                self.canvas_fwi(lat,log)#cria o grafico do indice FWI
        else:
            self.after(0,lambda: self.update_poi( [{'place': place, 'marker': None, 'distance': 0} for place in self.plaves_cash], lat, log))#se ja existirem os pontos no mapa, apenas atualiza as distancias
                
    
    #função que atualiza o marker
    def update_location(self, lat, log ,alt,dados_clima,marca,modelo,autonomia):
    
    #Adiciona e atualiza os graficos climaticos
        if not dados_clima:
            return
        else:
            add_graphs(dados_clima, self.temp_frame, self.vento_frame, self.hum_frame, self.pressao_frame)
            
        #Atualiza ou move o marcador do drone
        if hasattr(self, 'drone_marker') and self.drone_marker is not None:#se existir o marcador drone, ele apaga e atualiza com o novo marker
            self.drone_marker.delete()  
            self.drone_marker = None  

        #Se inicialmente nao existir marker, coloca o primeiro marker
        self.drone_marker = self.map_frame.set_marker(lat, log, icon = self.drone_marker_icon)
        
        ##atualiza labels do frame dos dados do drone e local
        if hasattr(self,'atualizar_labels'):
            self.atualizar_labels(lat,log,alt,dados_clima)
            self.atualizar_drone(marca,modelo,autonomia)
            
          
    
