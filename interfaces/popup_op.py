import tkinter as tk
from tkinter import simpledialog

class Popup(tk.Toplevel):
    def __init__(self, parent,set_user_name_callback):
        super().__init__(parent)
        
        self.title("Entrada do Nome")
        
        # Label e Entry para inserir o nome
        self.label = tk.Label(self, text="Digite seu nome:", font=("Arial", 12))
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(self, font=("Arial", 12))
        self.entry.pack(pady=10)
        
        # Botão para submeter o nome
        self.submit_button = tk.Button(self, text="Submeter", command=self.submit_name)
        self.submit_button.pack(pady=10)
        
        self.entry.focus()
        self.set_user_name_callback = set_user_name_callback

    def submit_name(self):
        #Método para pegar o nome da Entry e passá-lo para a Main_Page
        name = self.entry.get()
        if name:  # Verifica se o nome não está vazio
            self.set_user_name_callback(name) # Passa o nome para a Main_Page
            self.destroy()  # Fecha o pop-up
