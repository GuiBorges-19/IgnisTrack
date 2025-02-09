import tkinter as tk

def abrir_drone():
    janela = tk.Tk()
    janela.title("Drone Interface")
    janela.configure(bg="#f5f5f5")
    janela.geometry("600x400")
    
    drone_frame = tk.Frame(janela, bg="#D3D3D3", padx=10, pady=10)
    drone_frame.pack(padx=20, pady=10, fill="x")
    
    label_drone = tk.Label(drone_frame, text="Dados do Drone", font=("Arial", 12, "bold"), bg="#D3D3D3")
    label_drone.pack(anchor = "center")
    
    campos = ["Marca:","Modelo:", "Autonomia:"]
    for campo in campos:
        label = tk.Label(drone_frame, text=campo, font = ("Arial", 12, "bold", ),bg="#D3D3D3")
        label.pack(anchor="w")
        
    local_frame = tk.Frame(janela, bg="#D3D3D3", padx=10, pady=10)
    local_frame.pack(padx=20, pady=10, fill="x")
    
    title_local = tk.Label(local_frame, text="Ultima Localização:", font=("Arial", 12, "bold"), bg="#D3D3D3")
    title_local.pack(anchor="center")
    
    campos_local =  ["Latitude:", "Longitude:", "Altitude:"]
    for campo in campos_local:
        label = tk.Label(local_frame, text=campo,font = ("Arial", 12, "bold", ),bg="#D3D3D3")
        label.pack(anchor="w")
    

    janela.mainloop()
    
    

if __name__ == "__main__":
    abrir_drone()