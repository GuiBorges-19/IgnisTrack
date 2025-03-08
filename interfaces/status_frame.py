import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

def create_status_panel(parent):
    
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
    
    return status_frame, temp_frame,vento_frame,hum_frame,pressao_frame

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

"""def actual_label( labels_local, lat, log, alt):
   
    labels_local["Latitude:"].config(text=f"Latitude: {lat}")
    labels_local["Longitude:"].config(text=f"Longitude: {log}")
    labels_local["Altitude:"].config(text=f"Altitude: {alt}")"""


hist_temp = []
hist_vento = []
hist_humidade =  []
hist_pressao = []

def grafico_temp():
    if not hist_temp:
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
        return None
    
    fig,ax = plt.subplots(figsize=(4,3))
    
    
    ax.plot(hist_vento,color = "blue",marker ="o",linestyle = "-", label ="Vento(m/s)")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Temperatura: (ºC)")
    ax.legend()
    ax.grid(True)
    
    return fig


# Função para adicionar o gráfico dentro do frame no Tkinter
def add_graphs(dados_clima, temp_frame, vento_frame, hum_frame, pressao_frame):
    
    global hist_temp,hist_vento, hist_humidade, hist_pressao #permite mudar a variavel global
    
    hist_temp.append(dados_clima["temperatura"])
    hist_vento.append(dados_clima["vento"])
    hist_humidade.append(dados_clima["humidade"])
    hist_pressao.append(dados_clima["pressao"])

    
    if len(hist_temp) > 50:
        hist_temp.pop(0)
        
    if len(hist_vento) > 50:
        hist_vento.pop(0)
        
    if len(hist_humidade) > 50:
        hist_humidade.pop(0)
        
    if len(hist_pressao) > 50:
        hist_pressao.pop(0)
    
    """if not hasattr(add_graphs,"temp_data"):
        add_graphs.temp_data = []
        add_graphs.vento_data = []"""
        
    """temp = grafico_temp()
    vento = grafico_vento
    
    if temp is not None:
        add_graphs.temp_data.append(temp)
        
    if vento is not None:
        add_graphs.vento_data.append(vento)"""
    
    # Limpa os widgets existentes no frame antes de adicionar um novo gráfico

    for widget in temp_frame.winfo_children():
        widget.destroy()
    
    for widget in vento_frame.winfo_children():
        widget.destroy()
        
    for widget in hum_frame.winfo_children():
        widget.destroy()
    
    for widget in pressao_frame.winfo_children():
        widget.destroy()
        
    temp_graph = grafico_temp()
    vento_graph = grafico_vento()
    hum_graph = grafico_humidade()
    pressao_graph = grafico_pressao()
    
    
    if temp_graph:
        temp_canvas = FigureCanvasTkAgg(temp_graph, master = temp_frame)
        temp_canvas.draw()
        temp_canvas.get_tk_widget().grid(row=0,column=0, sticky="nsew")
        
    if vento_graph:
        temp_canvas = FigureCanvasTkAgg(vento_graph, master = vento_frame)
        temp_canvas.draw()
        temp_canvas.get_tk_widget().grid(row=1,column=0, sticky="nsew")
        
    if hum_graph:
        temp_canvas = FigureCanvasTkAgg(hum_graph, master = hum_frame)
        temp_canvas.draw()
        temp_canvas.get_tk_widget().grid(row=2,column=0, sticky="nsew")

    if pressao_graph:
        temp_canvas = FigureCanvasTkAgg(pressao_graph, master = pressao_frame)
        temp_canvas.draw()
        temp_canvas.get_tk_widget().grid(row=3,column=0, sticky="nsew")
    
 