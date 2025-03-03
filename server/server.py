import asyncio #ver para que servem estes importes
import websockets
import tkinter as tk
from threading import Thread

root = tk.Tk()
root.title("Monitor de Telemetria do Drone")
root.geometry("400x200")

label_dados = tk.Label(root, text="dados", font=("Arial", 14))
label_dados.pack(pady=20)


def data_atual(dados):
    label_dados.config(text=dados)
    
async def connect():
    uri = "ws://127.0.0.1:7890/telemetria"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Conectado ao server")
        
            while True:
                data = await websocket.recv()
                print(f"{data}")
                #atualiza na interface
                root.after(0,data_atual, data)
    except Exception as e:
        print(f"Erro: {e}")
        
        
def server_initial():

    asyncio.run(connect())

thread = Thread(target=server_initial, daemon=True)
thread.start()

root.mainloop()



