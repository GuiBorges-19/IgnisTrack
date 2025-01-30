import tkinter as tk
from tkinter import PhotoImage
from qgis.core import *
from qgis.gui import *
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import Qt


class MapWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Criação da janela Tkinter
        self.title("Mapa Interativo com PyQGIS e Tkinter")
        self.geometry("800x600")

        # Botão para carregar o mapa
        self.load_button = tk.Button(self, text="Carregar Mapa", command=self.load_map)
        self.load_button.pack(pady=10)

        # Canvas Tkinter para exibir a imagem do mapa
        self.canvas = tk.Label(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Inicializando a aplicação QGIS
        self.qgs_app = QgsApplication([], False)
        self.qgs_app.setPrefixPath("C:\\Program Files\\QGIS 3.34.14\\apps\\qgis-ltr\\python", True)  # Substitua pelo caminho certo do QGIS
        self.qgs_app.initQgis()

        # Criação do canvas do QGIS para renderização
        self.qgis_canvas = QgsMapCanvas()
        self.qgis_canvas.setCanvasColor(Qt.white)

    def load_map(self):
        # Carregar camada de exemplo
        layer = QgsVectorLayer("C:\\Program Files\\QGIS 3.34.14\\apps\\qgis-ltr\\python", "Camada de Exemplo", "ogr")  # Substitua pelo caminho correto
        if not layer.isValid():
            print("Erro ao carregar a camada!")
            return

        # Adicionar camada ao mapa
        QgsProject.instance().addMapLayer(layer)
        self.qgis_canvas.setExtent(layer.extent())

        # Renderizar o mapa para uma imagem
        self.render_map_to_image()

    def render_map_to_image(self):
        # Define a resolução da imagem gerada
        width, height = 800, 600

        # Criação de uma imagem para renderização
        image = QImage(width, height, QImage.Format_RGB32)
        image.fill(Qt.white)

        # Usamos um QPainter para desenhar o mapa na imagem
        painter = QPainter(image)
        self.qgis_canvas.render(painter)
        painter.end()

        # Convertendo a imagem para um formato que o Tkinter possa exibir
        self.display_image(image)

    def display_image(self, image):
        # Converter a imagem para o formato que Tkinter pode exibir
        width, height = image.width(), image.height()
        data = image.bits().asstring(width * height * 4)
        photo = PhotoImage(width=width, height=height, data=data)

        # Exibir a imagem no canvas Tkinter
        self.canvas.config(image=photo)
        self.canvas.image = photo

    def closeEvent(self, event):
        # Fechar a aplicação QGIS corretamente
        self.qgs_app.exitQgis()
        event.accept()


if __name__ == "__main__":
    # Inicializando a aplicação Tkinter
    app = MapWindow()
    app.mainloop()
