import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from interfaces.main import Main_Page
from interfaces.status_frame import end_op
from unittest.mock import MagicMock, patch
from interfaces.Data_Base.coneection_1 import get_db
from interfaces.server_tcp import Server
import pytest
import subprocess
import time
import socket
import requests
import unittest
import requests

#Teste de integração entre servidor e frontend
def test_server_app_integration():
    main_page = Main_Page(parent= None, controller=None)
    servidor = Server()

    dados_telemetria = {
        "lat": 40.7128,
        "log": -74.0060,
        "alt": 120,
        "marca": "DJI",
        "modelo": "MAvic",
        "autonomia": 50,
        "clima": {"temperatura": 23, "humidade": 50, "vento": 5, "pressao": 1012}
        
    }

    main_page.update_location(
        
        dados_telemetria["lat"],
        dados_telemetria["log"],
        dados_telemetria["alt"],
        dados_telemetria["clima"],
        dados_telemetria["marca"],
        dados_telemetria["modelo"],
        dados_telemetria["autonomia"] 
    )

    assert main_page.drone_marker is not None
    
#Teste de integração entre o servidor e a base de dados
@pytest.fixture
def db_connection():
    conn = get_db()
    if conn is None:
        pytest.fail("Conexão com a base de dados falhou")
    yield conn
    conn.close()
    
def test_server_database(db_connection):
    server = Server()
    server.first_lat = 40.7128
    server.first_log = -74.0060
    server.first_alt = 120
    
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO CoordenadasOperacao (latitude, longitude, altitude) VALUES (%s, %s, %s)",
                   (server.first_lat, server.first_log, server.first_alt))
    db_connection.commit()

    cursor.execute("SELECT latitude, longitude, altitude FROM CoordenadasOperacao ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()

    assert result == (server.first_lat, server.first_log, server.first_alt), "Valores inconsistentes entre server e DB"
    cursor.close()
    
#Teste de integração entre o servidor e o Drone

def start_server_process():
    
    process = subprocess.Popen(["python", "C:/Users/nicom/OneDrive/Desktop/Projeto_Ignistrack/interfaces/server_tcp.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  
    return process

@pytest.fixture
def start_server():

    server_process = start_server_process()
    yield server_process

    server_process.terminate()

def test_server_drone_integration(start_server):

    drone_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        drone_socket.connect(("127.0.0.1", 9999))  
        print("Conectado ao servidor!")

     
        lat = 40.7128
        log = -74.0060
        alt = 120
        marca = "DJI"
        modelo = "Phantom 4"
        autonomia = "30"

        # Formato da mensagem para o servidor
        message = f"{lat},{log},{alt},{marca},{modelo},{autonomia}"
        
        # Envia os dados para o servidor
        drone_socket.send(message.encode())
        
        # Aguarda um pouco para garantir que o servidor processou os dados
        time.sleep(1)
      
        assert True  # Verificação do sucesso da conexão

    except Exception as e:
        pytest.fail(f"Erro de conexão: {e}")
    finally:
        drone_socket.close()  # Fecha a conexão do drone simulado

#Teste de integração com a API

class TestOpenWeatherAPI(unittest.TestCase):
    def setUp(self):
        # Coordenadas de teste (Lisboa, por exemplo)
        self.lat = 38.7169
        self.lon = -9.1399
        self.api_key = "16e875e9b38c2081419f66dc2af10bf8"
        self.url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.api_key}&units=metric"

    def test_connection_and_data(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200, f"Falha ao conectar à API. Status code: {response.status_code}")

        data = response.json()

        # Verificar se os campos essenciais existem
        self.assertIn("main", data, "Campo 'main' não encontrado nos dados")
        self.assertIn("temp", data["main"], "Temperatura não encontrada")
        self.assertIn("humidity", data["main"], "Humidade não encontrada")
        self.assertIn("pressure", data["main"], "Pressão não encontrada")
        self.assertIn("wind", data, "Campo 'wind' não encontrado")
        self.assertIn("speed", data["wind"], "Velocidade do vento não encontrada")

        # Verificar tipos dos valores
        self.assertIsInstance(data["main"]["temp"], (int, float))
        self.assertIsInstance(data["main"]["humidity"], int)
        self.assertIsInstance(data["main"]["pressure"], int)
        self.assertIsInstance(data["wind"]["speed"], (int, float))

    def test_invalid_api_key(self):
        # Usando uma chave falsa para testar erro
        invalid_url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid=INVALID_KEY&units=metric"
        response = requests.get(invalid_url)
        self.assertEqual(response.status_code, 401, "Esperava código 401 para chave inválida")

