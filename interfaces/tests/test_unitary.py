import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import pytest
from interfaces.main import Main_Page 
import interfaces.status_frame as status_frame
from unittest.mock import patch, MagicMock
import tkinter as tk

# Teste de conexão com a Base de Dados
def test_connection_bd():
    from interfaces.Data_Base.coneection_1 import get_db
    conexao = get_db()
    assert conexao is not None, "Falha na conexão"
    assert conexao.is_connected() is True

# Teste de distância entre dois pontos
def test_dist_point():
    lat1, log1 = 38.7169, -9.1399  # Lisboa
    lat2, log2 = 41.1496, -8.6109  # Porto
    dist = Main_Page.dist_point(lat1, log1, lat2, log2)
    assert abs(dist / 1000 - 274) <= 5  

# Teste da classificação FWI
def test_fwi_class():
    main_page = Main_Page(parent=None, controller=None)
    
    assert main_page.fwi_classification(2)[0] == "Baixo"
    assert main_page.fwi_classification(10)[0]  == "Moderado"
    assert main_page.fwi_classification(20)[0]  == "Elevado"
    assert main_page.fwi_classification(60)[0]  == "Extremo"

# Teste do cálculo de FWI
def test_calculate_fwi():
    main_page = Main_Page(parent=None, controller=None) 
    fwi = main_page.get_fwi(41.1496, -8.6109)  
    assert fwi is not None

@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock:
        yield mock

def test_get_coordinates_sucess(mock_requests_get):
    mock_requests_get.return_value.json.return_value = {
        "status": "OK",
        "results": [{
            "geometry": {
                "location": {"lat": 41.1496, "lng": -8.6109}
            }
        }]
    }

    # Testa a função get_coordinates
    main_page = Main_Page(parent=None, controller=None)
    main_page.get_coordinates("Porto")

@patch("requests.get")
def test_get_distance_estrada(mock_requests_get):
    mock_requests_get.return_value.status_code = 200  
    mock_requests_get.return_value.json.return_value = {
        "status": "OK",
        "rows": [{
            "elements": [{
                "distance": {"text": "274 km"},  
                "duration": {"text": "10 mins"}
            }]
        }]
    }

    main_page = Main_Page(parent=None, controller=None)
    distancia, tempo = main_page.get_distance_estrada(40.7128, -74.0060, 34.0522, -118.2437)

    assert distancia == "274 km"
    assert tempo == "10 mins"
    

def test_update_location():
    main_page = Main_Page(parent=None, controller=None)
    main_page.drone_marker = None #marker do drone nao inserido
    
    lat,log,alt = 40.7128, -74.0060,100
    dados_clima = {"temperatura": 25,"humidade": 60,"vento": 5,"pressao": 1020}
    main_page.update_location(lat,log,alt,dados_clima, "DJI", "Mavic",60)
    
    #verifica se criou o marker
    assert main_page.drone_marker is not None

def test_display_places_on_canvas():
    main_page = Main_Page(parent=None, controller=None)
    
    places = [
        {"name": "Place 1","geometry": {"location": {"lat": 40.7128, "lng": -74.0060 }}}
    ]
    
    lat,log = 40.7128, -74.0060
    main_page.display_places_on_canvas(places,lat,log)
    
    assert len(main_page.info_panel.winfo_children()) > 0
    
def test_update_poi():
    
    main_page = Main_Page(parent=None, controller=None)
    
    places = [
        {"place": {"name": "Place 1", "geometry": {"location": {"lat": 40.7128, "lng": -74.0060 }}}, "distance" : "10m"}
    ]
    
    lat,lon = 40.7128, -74.0060
    main_page.update_poi(places, lat,lon)
    
    assert len(main_page.info_panel.winfo_children()) > 0
    
    
# testar a forma de adicionar os graficos
def test_add_graphs():
    status_frame.hist_temp = []
    status_frame.hist_vento = []
    status_frame.hist_humidade = []
    status_frame.hist_pressao = []
    status_frame.last_values = {"temperatura": None, "vento": None, "humidade": None, "pressao": None}
    status_frame.last_up_temp = 0
    status_frame.last_up_vento = 0
    status_frame.last_up_hum = 0
    status_frame.last_up_pres = 0
    status_frame.THRESHOLDS = {"temperatura":0.5,"vento":0.3,"humidade":2,"pressao":0.8}
    
    dados_clima = {"temperatura": 25,"humidade": 60,"vento": 5,"pressao": 1020}
    
    frame = tk.Frame()
    
    with patch("interfaces.status_frame.create_graph") as mock_create_graph, \
        patch("interfaces.status_frame.update_graph") as mock_update_graph:
            
            status_frame.add_graphs(dados_clima,frame,frame,frame,frame)
            assert mock_update_graph.call_count == 4
    
