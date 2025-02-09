from dronekit import connect
import pymysql
 
# Conectar ao drone
drone = connect('127.0.0.1:3306', wait_ready=True)
 
# Conectar ao MySQL
connection = pymysql.connect(
    host='localhost:3306',
    user='root',
    password='guilherme',
    database='Drone_Data'
)
 
try:
    with connection.cursor() as cursor:
        # Coletar dados do drone
        latitude = drone.location.global_frame.lat
        longitude = drone.location.global_frame.lon
        altitude = drone.location.global_frame.alt
        data_type = 'telemetry'
        data_value = 'N/A'  # Pode ser substituído por dados específicos
 
        # Inserir dados na tabela
        sql = "INSERT INTO FlightData (latitude, longitude, altitude, data_type, data_value) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (latitude, longitude, altitude, data_type, data_value))
 
    # Confirmar a transação
    connection.commit()
finally:
    connection.close()
    