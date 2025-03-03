import tkinter as tk
import threading
from tkinter import simpledialog
from main import Main_Page
from config_area import Config_area
from relatorios import Relatorios
from config_page import Config
from PIL import Image, ImageTk
from server_tcp import Server
from popup_op import Popup

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Tela inteira ocupada
        self.state("zoomed")
    
        # Configuração layout principal
        self.rowconfigure(0, weight=1)  # Header
        self.rowconfigure(1, weight=1)  # Containers
        self.columnconfigure(0, weight=1)
        
        self.container = tk.Frame(self,bg="#f5f5f5")
        self.container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.container.rowconfigure(0, weight=2)
        self.container.columnconfigure(0, weight=1)
        self.rowconfigure(0,weight=1)


        self.pages = {}  # Dicionário para armazenar as páginas
        
        self.create_navigation()  # Criar navegação
        self.create_pages()  # Criar as páginas
        self.show_page("main")
        
        self.server = Server(callback=self.update_drone_status)
        threading.Thread(target=self.server.run, daemon=True).start()

    def create_navigation(self):
        header_frame = tk.Frame(self, height=80)
        header_frame.grid(row=0, column=0, sticky="ew")
        
        header_frame.configure(background="#2E5984", bg="#2E5984")
        
        #carregar o logo
        logo_path = "figures/logo.png"
        logo = Image.open(logo_path).resize((320,70), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(logo)
        
        #adicionar logo no header
        logo_label = tk.Label(header_frame, image=self.logo_img)
        logo_label.grid(row=0, column=0, columnspan=5, padx=10, pady=5, sticky="nsew")
        
        nav_frame = tk.Frame(header_frame, bg="#2E5984", height=40)
        nav_frame.grid(row=1, column=1, sticky="e", pady=20)
        
                
        pages = [
            ("Página Principal", "main", "figures/home(2).png"),
            ("Configurar Área", "config_area", "figures/wide(1).png"),
            ("Relatórios", "relatorios", "figures/report(1).png"),
            ("Configurações", "config_page", "figures/gear.png"),
        ]
       
        for i, (btn_text, page_name, icon_path) in enumerate(pages):
            # Carregar o ícone
            icon = Image.open(icon_path)
            icon = icon.resize((20, 20), Image.Resampling.LANCZOS)  # Redimensionar
            icon = ImageTk.PhotoImage(icon)
            
            button = tk.Button(
                nav_frame,
                text=btn_text,
                image=icon,
                compound="left",
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
            button.bind("<Enter>", lambda e, b=button: b.config(bg="#1E4A6E"))
            button.bind("<Leave>", lambda e, b=button: b.config(bg="#2E5984"))
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
        
    """def open_popup(self):
        # Mostra o popup
        def set_user_name(name):
            self.pages["main"].set_user_name(name)
            self.show_page("main")
            
        popup = Popup(self, set_user_name)
        popup.grab_set()"""
        
    def update_drone_status(self, lat, log, alt,drone_status):
        print(f"[DEBUG] Atualizando drone: {lat}, {log}, {alt}")
        
        if "main" in self.pages:
            main_page = self.pages["main"]
            if hasattr(main_page, "update_location"):
                self.after(0,main_page.update_location, lat, log, alt,drone_status)
        else:
            print("[ERRO] 'update_location' não existe")
        
if __name__ == "__main__":
    app = App() 
    app.mainloop()

