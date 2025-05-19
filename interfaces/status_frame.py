import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ttkbootstrap as tb
import mysql.connector
import cv2
from ttkbootstrap.style import Style
from ttkbootstrap.scrolled import ScrolledFrame 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
from PIL import Image,ImageTk
from interfaces.relatorios import Relatorios
from interfaces.server_tcp import Server
import queue
from datetime import datetime
from interfaces.Data_Base import coneection_1

server_instance = None
server = Server()


def create_status_panel( parent, controller, table):

    style = Style()
    style.configure("Custo.TFrame", background ="#D9D9D9" )
       
    #Criação do status_frames que fica por dentro do Scrool_frame
    status_frame = ScrolledFrame(parent,borderwidth = 2, relief="solid",bootstyle="light", style = "Custo.TFrame",height=200)
    status_frame.grid(row=0, column=0,padx=5,pady=5,sticky="nsew")
    
    status_frame.columnconfigure(0, weight=1)
    status_frame.columnconfigure(1,weight=1)

    # Label e Entry do Operador
    operador_label = ttk.Label(status_frame, text="Operador:", font=("Inter", 14), borderwidth=2, relief="solid")
    operador_label.grid(row=0, column=0, sticky="w", pady=5, padx=10)
    operador_entry = ttk.Entry(status_frame)
    operador_entry.grid(row=0, column=1, sticky="ew", pady=5, padx = 10)

    # Label e Entry da Área
    area_label = ttk.Label(status_frame, text="Área:", font=("Inter", 14),  borderwidth=2, relief="solid")
    area_label.grid(row=1, column=0, sticky="w", pady=2,padx=10)
    area_entry = ttk.Entry(status_frame)
    area_entry.grid(row=1, column=1, sticky="ew", pady=2,padx=10)
        
    #botao terminar
    terminar = tk.Button(
                status_frame,
                text="Terminar Operação",
                compound="left",
                bg="#2E5984",
                fg="white",  # Cor do texto
                font=("Arial", 12, "bold"),
                borderwidth=2,
                relief="flat",
                anchor="center",
                padx=10,
                pady=5,
                highlightthickness=0,
                command=lambda: end_op(table,operador_entry,area_entry)
            )    
    terminar.bind("<Enter>", lambda e: terminar.config(bg="#00BCD4"))
    terminar.bind("<Leave>", lambda e: terminar.config(bg="#2E5984"))
    terminar.grid(row=3,column=0,padx=10, pady=2,sticky="ew")
    
    
     # Botão "Drone: Ativo" 
    drone_status_label = tk.Label(
        status_frame, text="Drone: Ativo", font=("Inter", 14), bg="#2E5984" , cursor="hand2", borderwidth=2, relief="solid"
    )
    drone_status_label.grid(row=3, column=1,padx=10, pady=15, sticky= "ew")
    
    #frame image_frame
    
    image_frame = tk.Canvas(status_frame, height=160)
    image_frame.grid(row=5, column=0,columnspan= 2, sticky="ew", padx=70, pady=5)
    
    #Frame do graficos das temperaturas
    temp_frame = ttk.Frame(status_frame,  style = "Custo.TFrame")
    temp_frame.grid(row=11, column=0, columnspan=2, sticky="ew",padx=30, pady=5)
    
    #Frame do graficos do vento
    vento_frame = ttk.Frame(status_frame,  style = "Custo.TFrame")
    vento_frame.grid(row=12, column=0, columnspan=2, sticky="ew",padx=30, pady=5)
    
    #Frame do graficos das temperaturas
    hum_frame = ttk.Frame(status_frame,  style = "Custo.TFrame")
    hum_frame.grid(row=13, column=0, columnspan=2, sticky="ew",padx=30, pady=5)
    
    #Frame do graficos do vento
    pressao_frame = ttk.Frame(status_frame,  style = "Custo.TFrame")
    pressao_frame.grid(row=14, column=0, columnspan=2, sticky="ew",padx=30, pady=5)
    
    iniciar_video(image_frame)
    
    return status_frame, temp_frame,vento_frame,hum_frame,pressao_frame, operador_entry,area_entry, 


def iniciar_video(image_frame):
    # Abre o vídeo com OpenCV
    cap = cv2.VideoCapture("Figures/aaaa.mp4")  # Caminho para o vídeo

    def mostrar_video():
        ret, frame = cap.read()

        if ret:
            # Redimensiona o vídeo para um tamanho menor
            scale = 0.15  
            frame = cv2.resize(frame, (int(frame.shape[1] * scale), int(frame.shape[0] * scale)))

            # Converte para o formato Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imagem_pil = Image.fromarray(frame_rgb)
            imagem_tk = ImageTk.PhotoImage(imagem_pil)

            # Atualiza a imagem no canvas
            image_frame.create_image(0, 0, image=imagem_tk, anchor=tk.NW)
            image_frame.image = imagem_tk  # Mantém a referência da imagem

            # Agenda a próxima atualização
            image_frame.after(5, mostrar_video)

        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reinicia o vídeo ao final
            image_frame.after(60, mostrar_video)

    # Inicia o loop do vídeo
    mostrar_video()


def create_drone_status(parent):
    """Cria o painel de status do drone."""
    frame_2 = ttk.Frame(parent, borderwidth=2, relief="solid", style="Custo.TFrame")
    frame_2.grid(row=0, column=1, sticky="nsew")

    # Configurar pesos para centralizar
    frame_2.grid_columnconfigure(0, weight=1)  # Margem esquerda
    frame_2.grid_columnconfigure(1, weight=0)  # Conteúdo
    frame_2.grid_columnconfigure(2, weight=1)  # Margem direita
    frame_2.grid_rowconfigure(0, weight=1)     # Margem superior
    frame_2.grid_rowconfigure(1, weight=0)     # Post-it drone
    frame_2.grid_rowconfigure(2, weight=0)     # Post-it localização
    frame_2.grid_rowconfigure(3, weight=0)     # Botão
    frame_2.grid_rowconfigure(4, weight=1)     # Margem inferior

    postit_style = {
        "bg": "#4B4B4B", "padx": 15, "pady": 15,
        "bd": 2, "relief": "raised"
    }

    # Post-it Drone
    postit_drone = tk.Frame(frame_2, **postit_style)
    postit_drone.grid(row=1, column=1, sticky="nsew", pady=(0, 15))

    label_drone = tk.Label(postit_drone, text="Dados do Drone", font=("Segoe UI", 13, "bold"), bg="#4B4B4B", fg="white")
    label_drone.grid(row=0, column=0, pady=(0, 10), sticky="nsew")

    campos = {}
    for i, campo in enumerate(["Marca:", "Modelo:", "Autonomia:"]):
        label = tk.Label(postit_drone, text=f"{campo} ---", font=("Segoe UI", 11, "bold"), bg="#4B4B4B", fg="white", anchor="w")
        label.grid(row=i+1, column=0, sticky="w", pady=3)
        campos[campo] = label

    # Post-it Localização
    postit_local = tk.Frame(frame_2, **postit_style)
    postit_local.grid(row=2, column=1, sticky="nsew", pady=(0, 15))

    title_local = tk.Label(postit_local, text="Última Localização:", font=("Segoe UI", 13, "bold"), bg="#4B4B4B", fg="white", anchor="w")
    title_local.grid(row=0, column=0, pady=(0, 10), sticky="nsew")

    labels_local = {}
    for i, campo in enumerate(["Latitude:", "Longitude:", "Altitude:"]):
        label = tk.Label(postit_local, text=f"{campo} ---", font=("Segoe UI", 11, "bold"), bg="#4B4B4B", fg="white", anchor="w")
        label.grid(row=i+1, column=0, sticky="w", pady=3)
        labels_local[campo] = label

    # Botão Voltar
    voltar_btn = tk.Button(
        frame_2,
        text="Voltar",
        compound="left",
        bg="#2E5984",
        fg="white",
        font=("Arial", 12, "bold"),
        borderwidth=2,
        relief="flat",
        anchor="center",
        padx=10,
        pady=5,
        highlightthickness=0
    )
    voltar_btn.grid(row=3, column=1, pady=10)
    voltar_btn.bind("<Enter>", lambda e: voltar_btn.config(bg="#00BCD4"))
    voltar_btn.bind("<Leave>", lambda e: voltar_btn.config(bg="#2E5984"))
    

    def atualizar_labels_na_interface(lat, log, alt, dados_clima):
        labels_local["Latitude:"].config(text=f"Latitude: {lat:.6f}")
        labels_local["Longitude:"].config(text=f"Longitude: {log:.6f}")
        labels_local["Altitude:"].config(text=f"Altitude: {alt:.2f} m")

    def atualizar_drone(marca, modelo, autonomia):
        campos["Marca:"].config(text=f"Marca: {marca}")
        campos["Modelo:"].config(text=f"Modelo: {modelo}")
        campos["Autonomia:"].config(text=f"Autonomia: {autonomia}")

        drone_info = {}
        drone_info["marca"] = marca
        drone_info["modelo"] = modelo
        drone_info["autonomia"] = autonomia
        

    return frame_2, labels_local, atualizar_labels_na_interface, atualizar_drone

hist_temp = []
hist_vento = []
hist_humidade =  []
hist_pressao = []

#ultimos valores para comparar como os novos valores
last_values = {
    "temperatura":None,
    "vento":None,
    "humidade":None,
    "pressao":None
}
#valores de mudança minimo para atualizar grafico
THRESHOLDS = {
    "temperatura":0.5,
    "vento":0.3,
    "humidade":2,
    "pressao":0.8
}

drone_info = {
    "marca": None,
    "modelo": None,
    "autonomia": None
}


def create_graph(dados,cor,label,ylabel):
    if not dados:
        print(f"Histórico de {label} está vazio.")
        return None
    
    fig,ax = plt.subplots(figsize=(3.5,2.5))
    ax.plot(dados,color = cor, marker = "o",markersize = 4,linewidth = 1.8, linestyle ="-", label = label)
    ax.set_xlabel("Tempo",fontsize = 9)
    ax.set_ylabel(ylabel, fontsize = 9)
    ax.legend(fontsize = 8, loc = "upper right")
    ax.grid(True, linestyle = "--", alpha = 0.5)
    ax.set_facecolor("#f8f9fa")
    ax.patch.set_facecolor("#f8f9fa")
    fig.tight_layout()

    
    return fig

def create_empty_graphs(temp_frame, vento_frame, hum_frame, pressao_frame):
    # Dados iniciais vazios (10 pontos com valor 0)
    initial_data = [0] * 10
    
    # Criar gráficos vazios
    temp_graph = create_graph(initial_data, "red", "Temperatura(ºC)", "Temperatura(ºC)")
    vento_graph = create_graph(initial_data, "blue", "Vento(m/s)", "Vento(m/s)")
    hum_graph = create_graph(initial_data, "black", "Humidade", "Humidade(%)")
    pressao_graph = create_graph(initial_data, "green", "Pressão", "Pressão(hPa)")
    
    # Adicionar gráficos aos frames
    for graph, frame in [
        (temp_graph, temp_frame),
        (vento_graph, vento_frame),
        (hum_graph, hum_frame),
        (pressao_graph, pressao_frame)
    ]:
        if graph:
            canvas = FigureCanvasTkAgg(graph, master=frame)
            canvas.draw()
            widget_canvas = canvas.get_tk_widget()
            widget_canvas.grid(row=0, column=0, sticky="nsew")

#Função que guarda os valores climaticos na bd
def save_temmp(cursor,operacao_id):
    if not hist_temp or not hist_vento or not hist_humidade or not hist_pressao:
        print("Arrays Vazias")
        return

    temp_media = sum(hist_temp) / len(hist_temp)
    vento_media = sum(hist_vento) / len(hist_vento)
    humidade_media = sum(hist_humidade) / len(hist_humidade)
    pressao_media = sum(hist_pressao) / len(hist_pressao)

    try:
        cursor.execute("SELECT id FROM CoordenadasOperacao ORDER BY id DESC LIMIT 1")
        coordenadas = cursor.fetchone()
        if not coordenadas:
            print("Erro, não encontra a coordenada")
            return

        cursor.execute("""
            INSERT INTO Clima (temperatura_media, vento, humidade, pressao,
                               ultravioleta, sensacao_termica, ponto_orvalho, qualidade_ar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (temp_media, vento_media, humidade_media, pressao_media, None, None, None, None))

        clima_id = cursor.lastrowid
        cursor.execute("UPDATE DataOperacao SET clima_id = %s WHERE id = %s", (clima_id, operacao_id))

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        raise 

#função que guarda os valores do drone na bd
def save_drone(cursor,marca,modelo,autonomia, operacao_id):
    try:
        cursor.execute("SELECT id FROM CoordenadasOperacao ORDER BY id DESC LIMIT 1")
        coordenadas = cursor.fetchone()
        if not coordenadas:
            print("Erro, não encontra a coordenada")
            return

        cursor.execute("""
            INSERT INTO Drone (marca,modelo,autonomia) VALUES (%s, %s, %s)
        """, (marca,modelo,autonomia))

        drone_id = cursor.lastrowid
        cursor.execute("UPDATE DataOperacao SET drone_id = %s WHERE id = %s", (drone_id, operacao_id))

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        raise 
    
    
        
last_up_temp = time.time()
last_up_vento = time.time()
last_up_hum = time.time()
last_up_pres = time.time()


# Função para adicionar o gráfico dentro do frame no Tkinter
def add_graphs(dados_clima, temp_frame, vento_frame, hum_frame, pressao_frame):
    
    global hist_temp,hist_vento, hist_humidade, hist_pressao #permite mudar a variavel global
    global last_up_temp, last_up_vento, last_up_hum, last_up_pres
    global last_values
    
    current_time = time.time()
    
    hist_temp.append(dados_clima["temperatura"])
    hist_vento.append(dados_clima["vento"])
    hist_humidade.append(dados_clima["humidade"])
    hist_pressao.append(dados_clima["pressao"])
    
    ##manetem os ultimos 50 valores nas listas
    hist_temp = hist_temp[-50:]
    hist_vento = hist_vento[-50:]
    hist_humidade = hist_humidade[-50:]
    hist_pressao = hist_pressao[-50:]
    
    def update_graph_marker(tipo,novo_valor,ultimo_valor,last_update):
        if ultimo_valor is None:
            return True
        if abs(novo_valor-ultimo_valor )>=THRESHOLDS[tipo]:
            return True
        if time.time() - last_update >=30:
            return True
        return False
    
    if update_graph_marker("temperatura", dados_clima["temperatura"], last_values["temperatura"], last_up_temp):
        last_up_temp = current_time
        last_values["temperatura"] = dados_clima["temperatura"]
        temp_graph = create_graph(hist_temp, "red", "Temperatura(ºC)", "Temperatura(ºC)")
        update_graph(temp_graph,temp_frame)
    
    if update_graph_marker("vento", dados_clima["vento"], last_values["vento"], last_up_vento):
        last_up_vento = current_time
        last_values["vento"] = dados_clima["vento"]
        temp_graph = create_graph(hist_vento, "blue", "Vento(m/s)", "Vento(m/s)")
        update_graph(temp_graph,vento_frame)
        
    if update_graph_marker("humidade", dados_clima["humidade"], last_values["humidade"], last_up_hum):
        last_up_hum = current_time
        last_values["humidade"] = dados_clima["humidade"]
        temp_graph = create_graph(hist_humidade, "black", "Humidade", "Humidade(%)")
        update_graph(temp_graph,hum_frame)
        
    if update_graph_marker("pressao", dados_clima["pressao"], last_values["pressao"], last_up_pres):
        last_up_pres = current_time
        last_values["pressao"] = dados_clima["pressao"]
        temp_graph = create_graph(hist_pressao, "green", "Pressão", "Pressão(hPa)")
        update_graph(temp_graph,pressao_frame)
    

def update_graph(graph, frame):
    for widget in frame.winfo_children():
        widget.destroy()
        
    canvas = FigureCanvasTkAgg(graph, master=frame)
    canvas.draw()
    widget_canvas = canvas.get_tk_widget() 
    widget_canvas.grid(row=0, column=0, sticky="nsew")

server_instance = Server()

 
def end_op(table, operador_entry, area_entry):
    global server_instance
    
    if server_instance is None:
        print("Erro: server_instance não foi iniciado corretamente.")
        messagebox.showerror("Erro", "O servidor não está a rodar.")
        return

    server_instance.set_callbacks()

    op_nome = operador_entry.get()
    area_nome = area_entry.get()

    if not op_nome or not area_nome:
        messagebox.showerror("Erro", "Por favor, insira o nome do operador e o nome da área.")
        return

    conexao = coneection_1.get_db()

    try:
        cursor = conexao.cursor(buffered=True)

        cursor.execute("SELECT id FROM CoordenadasOperacao ORDER BY id DESC LIMIT 1")
        resultado = cursor.fetchone()
        coordenadas_id = resultado[0] if resultado else None
        print(f"Última coordenada encontrada: {coordenadas_id}")

        cursor.execute("SELECT id FROM operador WHERE nome = %s", (op_nome,))
        resultado = cursor.fetchone()
        operador_id = resultado[0] if resultado else None
        if operador_id is None:
            cursor.execute("INSERT INTO operador (nome) VALUES (%s)", (op_nome,))
            operador_id = cursor.lastrowid

        cursor.execute("SELECT id FROM Areas WHERE nome_area = %s", (area_nome,))
        resultado = cursor.fetchone()
        area_id = resultado[0] if resultado else None
        if area_id is None:
            cursor.execute("INSERT INTO Areas (nome_area) VALUES (%s)", (area_nome,))
            area_id = cursor.lastrowid

        cursor.execute("INSERT INTO DataOperacao (operador_id, coordenadas_id, data) VALUES (%s, %s, NOW())",
                       (operador_id, coordenadas_id))
        operacao_id = cursor.lastrowid

        save_temmp(cursor, operacao_id)
        save_drone(cursor,drone_info["marca"],drone_info["modelo"],drone_info["autonomia"],operacao_id )

        cursor.execute("INSERT INTO OperacaoArea (operacao_id, area_id) VALUES (%s, %s)", (operacao_id, area_id))


        table.insert(
            "", "end",
            values=(op_nome, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    server_instance.first_lat, server_instance.first_log, server_instance.first_alt)
        )

        conexao.commit()
        messagebox.showinfo("Sucesso", "Operação guardada e finalizada com sucesso")

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        conexao.rollback()
        messagebox.showerror("Erro", "Erro ao guardar na base de dados")

    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()
        server_instance = None
