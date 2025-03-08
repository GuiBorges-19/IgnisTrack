import tkinter as tk
from tkinter import ttk
import mysql.connector
from datetime import datetime

class Relatorios(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.table_frame = tk.Frame(self, padx=20,pady=20,bg="#f0f0f0")
        self.table_frame.pack(expand=True,fill="both")
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        
        
        self.create_table()
        
        
    def create_table(self):
        style = ttk.Style()
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
        self.table.column("observacoes", width="200", anchor="center")
        
        self.table.grid(row=0,column=0,sticky="nsew")
        
        #scrollbar 
        scroll = ttk.Scrollbar(self.table_frame, orient="vertical",command=self.table.yview)
        self.table.configure(xscrollcommand=scroll.set)
        scroll.grid(row=0,column=1,sticky="ns")
        
        self.table_frame.grid_columnconfigure(0,weight=1)
        self.table_frame.grid_rowconfigure(0,weight=1)
        
    def load_data(self):
        try:
            conexao = mysql.connector.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    password='guilherme',
                    database='drone_project'
    )
            cursor = conexao.cursor()
            
            query = """select 
            Operador.nome as nome,
            DataOperacao.id as operacao_id,
            CoordenadasOperacao.latitude,
            CoordenadasOperacao.longitude,
            CoordenadasOperacao.altitude,
            Areas.nome_area
            
            From DataOperacao
            join Operador on DataOperacao.operador_id = Operador.id
            join CoordenadasOperacao on DataOperacao.coordenadas_id = CoordenadasOperacao.id
            join OperacaoArea on DataOperacao.id = OperacaoArea.operacao_id
            join Areas on OperacaoArea.area_id = area_id;"""
            
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            
            for row in rows:
                print(row)
                self.table.insert("","end",values=row)
                
            cursor.close()
            conexao.close()
                
        except mysql.connector.Error as e:
            print(f"Erro ao conectar:{e}")
        

     
        

    