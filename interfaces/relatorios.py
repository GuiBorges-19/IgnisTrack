import tkinter as tk
from tkinter import ttk
import mysql.connector
import ttkbootstrap as tb
from interfaces.Data_Base import coneection_1
from datetime import datetime

class Relatorios(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.table_frame = tk.Frame(self, padx=20,pady=20,bg="#f0f0f0")
        self.table_frame.pack(expand=True,fill="both")
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        
        #guarda as informações pra quando se expande a linha aparecer
        self.expand_rows = {}
        
        #filtro de pesquisa da tabela
        self.create_filter()
        
        #criação da tabela 
        self.create_table()
        
        
        self.load_data_bd()
            
    def create_table(self):
        style = tb.Style()
        style.configure("Treeview", font = ("Arial", 12), rowheight = 30,borderwidth = 1,relief = "solid")
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#007ACC", foreground="white")
        style.map("Treeview", background=[("selected", "#347083")])  # Cor de seleção
        
        self.table = ttk.Treeview(
            self.table_frame, 
            columns=("name","date","latitude","longitude","observacoes"),
            show="headings",
            style="Treeview"
        )
        
        #Criação dos cabeçalhos da tabela
        self.table.heading("name", text="Nome do Operador")
        self.table.heading("date", text = "Data")
        self.table.heading("latitude", text="Latitude")
        self.table.heading("longitude", text="Longitude")
        self.table.heading("observacoes", text="Obervações")
        
        
        #tamanho das colunas
        self.table.column("name", width="200", anchor="center")
        self.table.column("date", width="200", anchor="center")
        self.table.column("latitude", width="200", anchor="center")
        self.table.column("longitude", width="200", anchor="center")
        self.table.column("observacoes", width="400", anchor="center")
        self.table.tag_configure("child", background="#f2f2f2", font= ("Arial",11, "italic"))
        self.table.grid(row=0,column=0,sticky="nsew")
        
        #scrollbar 
        scroll = ttk.Scrollbar(self.table_frame, orient="vertical",command=self.table.yview)
        self.table.configure(xscrollcommand=scroll.set)
        scroll.grid(row=0,column=1,sticky="ns")
        
        self.table_frame.grid_columnconfigure(0,weight=1)
        self.table_frame.grid_rowconfigure(0,weight=1)
        
        self.table.bind("<Button-1>", self.on_click)
        
    #Função que carrega os dados da base de dados
    def load_data_bd(self):
        
        ##conexao ao mysql
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                port=3306,
                user='root',
                password='guilherme',
                database='drone_project'
            )
            cursor = conexao.cursor()

        #query que pesquisa os dados de uma operação registada na base de dados
            query = """select 
            Operador.nome as nome,
            DataOperacao.data AS data_operacao,
            CoordenadasOperacao.latitude,
            CoordenadasOperacao.longitude,
            CoordenadasOperacao.altitude,
            Areas.nome_area,
            Clima.temperatura_media,
            Clima.vento,
            Clima.humidade,
            Clima.pressao
            
            From DataOperacao
            join Operador on DataOperacao.operador_id = Operador.id
            join CoordenadasOperacao on DataOperacao.coordenadas_id = CoordenadasOperacao.id
            join OperacaoArea on DataOperacao.id = OperacaoArea.operacao_id
            join Areas on OperacaoArea.area_id = Areas.id
            left join Clima on DataOperacao.clima_id = Clima.id;"""
        
            #executa a query
            cursor.execute(query)
            
            #resultado é o que é encontrado na pesquisa
            resultado = cursor.fetchall()
            
            #limpa a tabela atual
            for row in self.table.get_children():
                self.table.delete(row)
                
            for row in resultado:
                op_nome, date, latitude, longitude, altitude, area, temperatura, vento, humidade, pressao = row
                
                if date is not None:
                    data_normal = date.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    data_normal = "Nada"
            
            #Insere os valores de cada operação na tabela e guarda no dicionario expand_rows dados extra 
                item_id = self.table.insert("","end",values=(op_nome, data_normal,latitude,longitude,"▶"))
            
                self.expand_rows[item_id] = (altitude,area,  temperatura, vento, humidade, pressao )
               
            cursor.close()
            conexao.close()

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            
    #Função que gere o cliuqe do utilisador no butão de expandir linha
    def on_click(self,event):
        
        #deteta a linha e a coluna clicadas
        row = self.table.identify_row(event.y)
        column = self.table.identify_column(event.x)
    
        #se nao clicou em nenhuma linha ou na coluna 5 sai da função
        if not row or column != "#5":
            return
        
        #nao expande linha expandidas
        if self.table.parent(row):
            return
       
       #verifica como se encontra a seta
        values = self.table.item(row, "values")
        
        #chama para expandir
        if values[4] == "▶":
            self.expand_row(row,values)
        
        ##chama para colapasar
        if values[4] == "▼":
            self.collapse_row(row)
    
    #função que expande a linha
    def expand_row(self,item_id,values):
        if item_id in self.expand_rows:
            altitude, area, temperatura, vento, humidade,pressao = self.expand_rows[item_id]
            print(self.expand_rows[item_id])
            col1 = f"Altitude: {altitude}"
            col2 = f"Nome da Área: {area}"
            col3 = f"Temperatura Média: {temperatura}"
            col4 = f"Vento: {vento}"
            col5 = f"Humidade: {humidade}| Pressão: {pressao}" 
            
            self.table.insert(item_id, "end", values=(col1,col2,col3,col4,col5), tags=("child",))
            
            self.table.item(item_id, values=(values[0],values[1], values[2],values[3],"▼"))
            
            self.expand_rows[item_id] = (altitude, area, temperatura, vento, humidade,pressao )
        
    #funçao que colapsa a linha
    def collapse_row(self,item_id):
        #vai buscar a linha colpsada
        children = self.table.get_children(item_id)
        
        for child in children:
            self.table.delete(child)
            
        values = self.table.item(item_id, "values")
        self.table.item(item_id, values=(values[0], values[1], values[2], values[3], "▶"))
            
    #função que cria o filtro    
    def create_filter(self):
        self.filter = tk.Frame(self, bg = "#D9D9D9")
        self.filter.pack(pady=10, fill="x")
        
        tk.Label(self.filter, text="Filtrar por Nome: ", bg="#f0f0f0").pack(side="left", padx=10)
        
        self.filter_entry = tk.Entry(self.filter)
        self.filter_entry.pack(side="left", padx=5)
        
        self.filter_b = tk.Button(self.filter,text="Filtrar", command=self.apply_filter)
        self.filter_b.pack(side="left", padx=5)
        
        self.filter.bind("<KeyRelease>", self.apply_filter)
        
    #quando chamada aplica o filtro
    def apply_filter(self):
        #vai buscar o nome ao filtro
        filtro = self.filter_entry.get().lower()
        
        
        for row in self.table.get_children():
            self.table.delete(row)
            
        try:
            conexao = coneection_1.get_db()
            cursor = conexao.cursor()

            # Consulta para buscar os dados
            query = """select DISTINCT
            Operador.nome as nome,
            DataOperacao.data AS data_operacao,
            CoordenadasOperacao.latitude,
            CoordenadasOperacao.longitude,
            CoordenadasOperacao.altitude,
            Areas.nome_area,
            Clima.temperatura_media,
            Clima.vento,
            Clima.humidade,
            Clima.pressao
            
            From DataOperacao
            join Operador on DataOperacao.operador_id = Operador.id
            join CoordenadasOperacao on DataOperacao.coordenadas_id = CoordenadasOperacao.id
            join OperacaoArea on DataOperacao.id = OperacaoArea.operacao_id
            join Areas on OperacaoArea.area_id = Areas.id
            left join Clima on DataOperacao.clima_id = Clima.id
            where Operador.nome Like %s;"""
            
            #faz a pesquisa aplicando o filtro
            cursor.execute(query, (f"%{filtro}%",))
            resultado = cursor.fetchall()
            
            for row in resultado:
                op_nome, date, latitude, longitude, altitude, area, temperatura, vento, humidade, pressao = row                
                item_id = self.table.insert("", "end", values=(op_nome, date, latitude, longitude, "▶"))
                self.expand_rows[item_id] = (altitude, area, temperatura, vento,humidade,pressao)

            cursor.close()
            conexao.close()
            
        except mysql.connector.Error as err:
            print(f"Erro") 
        
  
    
