import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
import threading
from tkinter import ttk
from tkinter import simpledialog
from interfaces.config_area import Config_area
import collections
from ttkbootstrap.style import Style
from interfaces.relatorios import Relatorios
from interfaces.main import Main_Page
from interfaces.config_page import Config
from PIL import Image, ImageTk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Tela inteira ocupada
        self.state("zoomed")

        # Configuração layout principal
        self.rowconfigure(0, weight=1)  # Header
        self.rowconfigure(1, weight=1)  # Containers
        self.columnconfigure(0, weight=1)
           
        self.container = tk.Frame(self)
        self.container.grid(row=1, column=0, sticky="nsew", padx=10, pady=0)
        self.configure(bg="#2E5984")
        
        self.container.rowconfigure(0, weight=2)
        self.container.columnconfigure(0, weight=1)
        self.rowconfigure(0,weight=1)
        
        self.pages = {}  # Dicionário para armazenar as páginas
        
        self.create_navigation()  # Criar navegação
        self.create_pages()  # Criar as páginas
        self.show_page("main")
        
    #Função de criação da barra de navegação
    def create_navigation(self):
        
        style = Style()
        style.configure("Custom.TFrame", background ="#2E5984" )
        
        header_frame = ttk.Frame(self, style = "Custom.TFrame" )
        header_frame.grid(row=0, column=0, sticky="nsew")
        header_frame.columnconfigure(0, weight=1)
        
        #Logo da aplicação
        logo = Image.open("figures/logo.png").resize((320,70), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(logo)  

        #label para introduzir o logo
        logo_label = ttk.Label(header_frame, image= self.logo_img, background="#2E5984")
        logo_label.grid(row=0, column=0, columnspan=5, padx=600, pady=5, sticky="ew")
        
        #frame com os botões do menu da navegação
        nav_frame = ttk.Frame(header_frame)
        nav_frame.grid(row=1, column=1, sticky="e", pady=20)
        
                   
        pages = [
            ("Página Principal", "main", "figures/home(2).png"),
            ("Configurar Área", "config_area", "figures/wide(1).png"),
            ("Relatórios", "relatorios", "figures/report(1).png"),
            ("Configurações", "config_page", "figures/gear.png"),
        ]
        
        
       
        for i, (btn_text, page_name, icon_path) in enumerate(pages):
            # Carregar o ícone para cada button
            icon = Image.open(icon_path)
            icon = icon.resize((20, 20), Image.Resampling.LANCZOS)  # Redimensionar
            icon = ImageTk.PhotoImage(icon)
            
            button = tk.Button(
                nav_frame,
                text=btn_text,
                image=icon,
                compound="left",
                #bg="#2E5984",
                fg="white",  # Cor do texto
                font=("Arial", 14, "bold"),
                borderwidth=0,
                relief="flat",
                height=50,
                padx=10,
                pady=5,
                highlightthickness=0,
                command=lambda p=page_name: self.show_page(p),
            )
            button.image = icon  # Referência para evitar que a imagem seja descartada
            button.bind("<Enter>", lambda e, b = button: b.config(bg="#00BCD4"))
            button.bind("<Leave>", lambda e, b = button: b.config(bg="#2E5984"))
            button.grid(row=0, column=i, padx=5, pady=5)  # Distribuir igualmente

        # Garantir que os botões ocupem toda a largura
        for i in range(len(pages)):
            header_frame.columnconfigure(i, weight=1)
        
    def create_pages(self):
        # Criar todas as páginas e armazenar no dicionário
        self.pages["main"] = Main_Page(self.container, self)
        self.pages["config_area"] = Config_area(self.container, self)
        self.pages["relatorios"] = Relatorios(self.container, self)
        self.pages["config_page"] = Config(self.container, self)

        # Inserir todas as páginas no grid
        for page in self.pages.values():
            page.grid(row=0, column = 0 ,sticky="nsew")
                
    def show_page(self, page_name):
        #Mostra a página especificada
        page = self.pages[page_name]
        page.tkraise()

if __name__ == "__main__":
    app = App() 
    app.mainloop()