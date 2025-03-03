import tkinter as tk
from PIL import Image, ImageTk
from  qgis.core import *

import random
root = tk.Tk()
root.title("Mapa")

label = tk.Label(root)
label.pack()

mapa_path = r"C:\\Users\\nicom\\OneDrive - Ensino Lusófona\\3ºAno\\teste.qgz"

def actual_mapa():
    lon = -9.139
    lat = 38.716
    lon = random.uniform(-0.01,0.01)
    lat = random.uniform(-0.01,-0.01)
    
    actual_mapa(lon, lat)
    
    layout_manager = QgsProject.instance().layoutManager()
    layouts = layout_manager.layouts()
    
    if layouts:
        layout = layouts[0]
        exporter = QgsLayoutExporter(layout)
        exporter.exportToImage(mapa_path,QgsLayoutExporter.ImageExportSettings())
        
        imagem = Image.open(mapa_path)
        imagem = imagem.resize((800,600))
        photo = ImageTk.PhotoImage(imagem)
        label.config(image=photo)
        label.image = photo
        
    root.after(3000,actual_mapa)
    
actual_mapa()
root.mainloop()

        