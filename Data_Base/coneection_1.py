import mysql.connector as mysql

try:
  
    conexao = mysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='guilherme',
        database='Drone_Data'
    )
    cursor = conexao.cursor()
    print("Connection successful")

    """sql = "INSERT INTO CoordenadasOperacao (id, latitude, longitude, altitude, temperatura_media, velocidade_vento) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (22.9, -43.2, 100, '2023-10-10', 'aaaaa', 'aaaaaa')  # Example corrected values

    cursor.execute(sql, val)"""

    conexao.commit()

    print(f"{cursor.rowcount} record inserted.")
except mysql.Error as err:
    print(f"Error: {err}")
finally:
    
    if 'conexao' in locals() and conexao.is_connected():
        cursor.close()
        conexao.close()
