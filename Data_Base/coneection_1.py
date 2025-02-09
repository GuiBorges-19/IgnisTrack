import mysql.connector as mysql

try:
    # Establish the database connection
    conexao = mysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='guilherme',
        database='Drone_Data'
    )
    cursor = conexao.cursor()
    print("Connection successful")

    # SQL query and values
    sql = "INSERT INTO FlightData (latitude, longitude, altitude, data_type, data_value) VALUES (%s, %s, %s, %s, %s)"
    val = (22.9, -43.2, 100, '2023-10-10', 'aaaaa')  # Example corrected values

    # Execute the SQL query
    cursor.execute(sql, val)

    # Commit the changes to the database
    conexao.commit()

    print(f"{cursor.rowcount} record inserted.")
except mysql.Error as err:
    print(f"Error: {err}")
finally:
    # Close the connection
    if 'conexao' in locals() and conexao.is_connected():
        cursor.close()
        conexao.close()
