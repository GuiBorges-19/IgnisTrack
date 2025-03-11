import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ttkbootstrap as tb
import mysql.connector

from ttkbootstrap.scrolled import ScrolledFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
from relatorios import Relatorios
from server_tcp import Server
from datetime import datetime


server_instance = None


op_ativa = True

def create_status_panel( parent, controller, table):
    
    """#Container que ontem todos os frames do status_frames
    scroll_container = ScrolledFrame(parent, width=600, height=300)
    scroll_container.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")
    scroll_container.columnconfigure(0,weight=1)"""
    
    #Criação do status_frames que fica por dentro do Scrool_frame
    status_frame = ScrolledFrame(parent,borderwidth = 2, relief="solid")
    status_frame.grid(row=0, column=0, padx=2,pady=2,sticky="nsew")
    status_frame.columnconfigure(1, weight=1)
    
    status_frame.grid_configure(row=0, column=0, ipadx=5, ipady=5)  # Aumentar o padding se necessário
    status_frame.config(height=300)  # Definindo uma altura fixa de 300px
    
    
    # Label e Entry do Operador
    operador_label = ttk.Label(status_frame, text="Operador:", font=("Inter", 14))
    operador_label.grid(row=0, column=0, sticky="w", pady=5)
    operador_entry = ttk.Entry(status_frame)
    operador_entry.grid(row=0, column=1, sticky="ew", pady=5)

    # Label e Entry da Área
    area_label = ttk.Label(status_frame, text="Área:", font=("Inter", 14))
    area_label.grid(row=1, column=0, sticky="w", pady=5)
    area_entry = ttk.Entry(status_frame)
    area_entry.grid(row=1, column=1, sticky="ew", pady=5)
    
    
    # Botão "Drone: Ativo" 
    drone_status_label = tk.Label(
        status_frame, text="Drone: Ativo", font=("Inter", 14), fg="blue", cursor="hand2"
    )
    drone_status_label.grid(row=2, column=0, columnspan=2, pady=15)
    
    global server_instance
    if server_instance is None:
        server_instance = Server(callback= lambda lat, log, alt, dados_clima: status_frame.after(
            0,lambda: add_graphs(dados_clima, temp_frame,vento_frame,hum_frame, pressao_frame)
            )
        )
        server_instance.run()

    
    #botao terminar
    terminar = tk.Button(status_frame,text="Terminar Operação", command= lambda: end_op(table,operador_entry,area_entry))


    terminar.grid(row=3,column=0,pady=10)
    
    #Frame do graficos das temperaturas
    temp_frame = ttk.Frame(status_frame)
    temp_frame.grid(row=4, column=0, columnspan=2, sticky="nsew",pady=10)
    
    #Frame do graficos do vento
    vento_frame = ttk.Frame(status_frame)
    vento_frame.grid(row=5, column=0, columnspan=2, sticky="nsew",pady=10)
    
    #Frame do graficos das temperaturas
    hum_frame = ttk.Frame(status_frame)
    hum_frame.grid(row=6, column=0, columnspan=2, sticky="nsew",pady=10)
    
    #Frame do graficos do vento
    pressao_frame = ttk.Frame(status_frame)
    pressao_frame.grid(row=7, column=0, columnspan=2, sticky="nsew",pady=10)
    
    
    return status_frame, temp_frame,vento_frame,hum_frame,pressao_frame, operador_entry,area_entry



def create_drone_status(parent):
    """Cria o painel de status do drone."""
    frame_2 = tk.Frame(parent, bg="#D3D3D3", padx=20, pady=20)
    frame_2.grid(row=0, column=1, sticky="nsew")

    # Adicionando título e campos de dados
    label_drone = tk.Label(frame_2, text="Dados do Drone", font=("Arial", 14, "bold"), bg="#D3D3D3")
    label_drone.grid(row=0, column=0, pady=10, sticky="w")

    campos = ["Marca:", "Modelo:", "Autonomia:"]
    for i, campo in enumerate(campos):
        label = tk.Label(frame_2, text=campo, font=("Arial", 12, "bold"), bg="#D3D3D3")
        label.grid(row=i+1, column=0, sticky="w")

    local_frame = tk.Frame(frame_2, bg="#D3D3D3", padx=10, pady=10)
    local_frame.grid(row=len(campos)+1, column=0, sticky="nsew")

    title_local = tk.Label(local_frame, text="Última Localização:", font=("Arial", 12, "bold"), bg="#D3D3D3")
    title_local.grid(row=0, column=0, sticky="w")

    labels_local = {}
    for i, campo in enumerate(["Latitude:", "Longitude:", "Altitude:"]):
        label = tk.Label(local_frame, text=f"{campo} ---", font=("Arial", 12, "bold"), bg="#D3D3D3")
        label.grid(row=i+1, column=0, sticky="w")
        labels_local[campo] = label

    # Botão para voltar ao status_frame
    voltar_btn = tk.Button(frame_2, text="Voltar", bg="lightgray", font=("Arial", 12))
    voltar_btn.grid(row=len(campos)+len(labels_local)+2, column=0, pady=10)

    return frame_2, labels_local

hist_temp = []
hist_vento = []
hist_humidade =  []
hist_pressao = []

def grafico_temp():
    if not hist_temp:
        print("Histórico de temperatura está vazio.")
        return None
    
    fig,ax = plt.subplots(figsize=(4,3))
    
    ax.plot(hist_temp,color = "red", marker = "o", linestyle ="-", label ="Temperatura(ºC)")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Temperatura: (ºC)")
    ax.legend()
    ax.grid(True)
    
    return fig

def grafico_humidade():
    if not hist_humidade:
        print("Histórico de temperatura está vazio.")
        return None
    
    fig,ax = plt.subplots(figsize=(4,3))
    
    ax.plot(hist_humidade,color = "black", marker = "o", linestyle ="-", label ="Humidade")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Humidade")
    ax.legend()
    ax.grid(True)
    
    return fig
    
def grafico_pressao():
    if not hist_pressao:
        print("Histórico de temperatura está vazio.")
        return None
    
    fig,ax = plt.subplots(figsize=(4,3))
    
    ax.plot(hist_pressao,color = "green", marker = "o", linestyle ="-", label ="pressao")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Pressao")
    ax.legend()
    ax.grid(True)
    
    return fig
    


def grafico_vento():
    if not hist_vento:
        print("Histórico de temperatura está vazio.")
        return None
    
    fig,ax = plt.subplots(figsize=(4,3))
    
    
    ax.plot(hist_vento,color = "blue",marker ="o",linestyle = "-", label ="Vento(m/s)")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Temperatura: (ºC)")
    ax.legend()
    ax.grid(True)
    
    return fig

last_up_vento = time.time()
last_up_hum = time.time()
last_up_pres = time.time()


# Função para adicionar o gráfico dentro do frame no Tkinter
def add_graphs(dados_clima, temp_frame, vento_frame, hum_frame, pressao_frame):
    
    global hist_temp,hist_vento, hist_humidade, hist_pressao #permite mudar a variavel global
    global last_up_vento, last_up_hum, last_up_pres
    
    current_time = time.time()
    
    hist_temp.append(dados_clima["temperatura"])
    hist_vento.append(dados_clima["vento"])
    hist_humidade.append(dados_clima["humidade"])
    hist_pressao.append(dados_clima["pressao"])
    
    hist_temp = hist_temp[-50:]
    hist_vento = hist_vento[-50:]
    hist_humidade = hist_humidade[-50:]
    hist_pressao = hist_pressao[-50:]
    
    temp_graph = grafico_temp()
    if temp_graph:
        update_graph(temp_graph,temp_frame)
    
    if current_time - last_up_vento >= 20:
        last_up_vento = current_time
        vento_graph = grafico_vento()
        update_graph(vento_graph,vento_frame)
            
    if current_time - last_up_hum >=20:
        last_up_hum = current_time
        hum_graph = grafico_humidade()
        update_graph(hum_graph,hum_frame)
            
    if current_time - last_up_pres >=20:
        last_up_pres = current_time
        pressao_graph = grafico_pressao()
        update_graph(pressao_graph,pressao_frame)
    

def update_graph(graph, frame):
    for widget in frame.winfo_children():
        widget.destroy()
        
    canvas = FigureCanvasTkAgg(graph, master=frame)
    canvas.draw()
    widget_canvas = canvas.get_tk_widget() 
    widget_canvas.grid(row=0, column=0, sticky="nsew")
    
def end_op(table, operador_entry,area_entry):

        global server_instance
    
        op_nome =operador_entry.get()
        area_nome = area_entry.get()
        
        global op_ativa
        
        if server_instance is None:
            return
            
        if not op_nome or not area_nome:
            messagebox.showerror("Por favor, insira o nome do operador e o nome da área.")
            return
        
        if (server_instance.first_lat is None or server_instance.first_log is None or server_instance.first_alt is None):
                messagebox.showerror("Erro", "coordendas nao inseridas")
                return
            
        
        try: 
            server_instance.stop_server()
            conexao = mysql.connector.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    password='guilherme',
                    database='drone_project'
    )
            cursor = conexao.cursor(buffered=True)
            coordenadas_id = None
            
            cursor.execute("select id from operador where nome = %s", (op_nome,))
            resultado = cursor.fetchone()
            
            if resultado:
                operador_id = resultado[0]
            
            else:
                cursor.execute("insert into operador (nome) values (%s)", (op_nome,))
                operador_id = cursor.lastrowid
                
            cursor.execute("select id from Areas where nome_area = %s", (area_nome,))
            resultado = cursor.fetchone() 
               
            if resultado:
                area_id = resultado[0]
            else:
                cursor.execute("Insert into Areas (nome_area) values (%s)", (area_nome,))
                area_id = cursor.lastrowid
                
            cursor.execute("""Insert into CoordenadasOperacao(latitude,longitude,altitude)values(%s,%s,%s)""",
            (server_instance.first_lat, server_instance.first_log, server_instance.first_alt))
            coordenadas_id = cursor.lastrowid
            
            cursor.execute(
                """insert into DataOperacao (operador_id, coordenadas_id, data) values (%s,%s,Now())""",(operador_id,coordenadas_id)
            )
            operacao_id = cursor.lastrowid
            
            cursor.execute("""insert into OperacaoArea (operacao_id, area_id) values (%s,%s)""", (operacao_id,area_id))

            
            table.insert(
            "",  # Root
            "end",  # Colocar no final
            values = (op_nome, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), server_instance.first_lat, server_instance.first_log, area_nome)  # Dados das colunas
        )
            conexao.commit()
            cursor.close()
            conexao.close()
        
            op_ativa = False
            server_instance = None
            
            
            messagebox.showinfo("Sucesso", "Operação guardada e finalizada com Sucesso")
            
        
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
        
        op_ativa = False
      
    

    
    
    
    
    


