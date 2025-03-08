import tkinter as tk
from tkintermapview import TkinterMapView

class MapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mapa Interativo com Barra de Pesquisa")

        # Frame principal
        self.body_frame = tk.Frame(root)
        self.body_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Frame para conter a barra de pesquisa e o mapa
        self.map_container = tk.Frame(self.body_frame)
        self.map_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Criar barra de pesquisa acima do mapa
        search_frame = tk.Frame(self.map_container)
        search_frame.grid(row=0, column=0, sticky="ew", pady=5)

        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.grid(row=0, column=0, padx=5, pady=5)

        self.search_b = tk.Button(search_frame, text="Pesquisar", command=self.search_local)
        self.search_b.grid(row=0, column=1, padx=5, pady=5)

        # Criar o frame do mapa logo abaixo da barra de pesquisa
        self.map_frame = self.create_map_frame(self.map_container)
        self.map_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Configurar a expansão correta para ocupar espaço disponível
        self.map_container.grid_rowconfigure(1, weight=1)
        self.map_container.grid_columnconfigure(0, weight=1)

    def create_map_frame(self, parent):
        map_frame = TkinterMapView(parent, width=600, height=500, corner_radius=0)
        map_frame.set_tile_server("https://mt0.google.com/vt/lyrs=m&x={x}&y={y}&z={z}", max_zoom=22)
        map_frame.set_geocoder("https://geocode.maps.co/search?q={}", "nicomedio2003@gmail.com")
        map_frame.set_address("São Paulo, Brasil", marker=True)  # Localização inicial
        return map_frame

    def search_local(self):
        location = self.search_entry.get()
        if location:
            self.map_frame.set_address(location, marker=True)
        else:
            print("Local não encontrado")

# Criar janela principal
root = tk.Tk()
app = MapApp(root)
root.mainloop()
