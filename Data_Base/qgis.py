import sys
import os

# Defina o caminho do QGIS corretamente
os.environ['QGIS_PREFIX_PATH'] = "C:/Program Files/QGIS 3.34.14/apps/qgis-ltr"  # Altere conforme a versão

from qgis.core import QgsApplication, QgsProject, QgsVectorLayer, QgsMapCanvas

# Inicialize o QGIS
qgs = QgsApplication([], False)
qgs.initQgis()

# Criar o projeto e carregar a camada
project = QgsProject.instance()
layer = QgsVectorLayer("C:/Users/nicom/OneDrive - Ensino Lusófona/3ºAno/teste.qgz", "Minha Camada", "ogr")

if not layer.isValid():
    print("Falha ao carregar a camada.")
else:
    project.addMapLayer(layer)

# Configurando o mapa
canvas = QgsMapCanvas()
canvas.setExtent(layer.extent())
canvas.setLayers([layer])
canvas.show()

# Mantendo o QGIS ativo até que a janela seja fechada
qgs.exec_()

# Finalizando a aplicação QGIS
qgs.exitQgis()
