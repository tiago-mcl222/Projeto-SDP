import socket
import json
import mysql.connector
import threading
from cryptography.fernet import Fernet

HOST = '192.168.1.81'
PORT = 5656

current_user = None


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f'[*] Listening on HOST: {HOST} | PORT: {PORT}')

    while True:
        conn, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(conn, addr))
        client_handler.start()


# Function to query data from MySQL database (#3 camada)
def connect_to_database():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "Fc.porto.20",
        database = "client_server"
    )

def store_database(request):
    mydb = connect_to_database()
    mycursor = mydb.cursor()
    
    sql_formula = f"INSERT INTO notas (username, note) VALUES (%s, %s)"

    mycursor.execute(sql_formula, (current_user, request,))
    mydb.commit()

    mycursor.close() # Close the database connection
    mydb.close() # Close the database connection

def show_notes():
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    query = f"SELECT note_id, note FROM notas WHERE username = %s"
    mycursor.execute(query, (current_user,))
    result = mycursor.fetchall() # Fetch all rows

    mycursor.close() # Close the database connection
    mydb.close() # Close the database connection

    return result

def select_notes(client_note_id):
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    query = f"SELECT note FROM notas WHERE note_id = %s"
    mycursor.execute(query, (client_note_id,))
    result = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return result

def update_database(client_note_id, modified_note):
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    sql = f"UPDATE notas SET note = %s WHERE note_id = %s"
    mycursor.execute(sql, (modified_note, client_note_id,))
    mydb.commit()

    mycursor.close() # Close the database connection
    mydb.close() # Close the database connection

def delete_notes(client_note_id):
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    sql = f"DELETE from notas WHERE note_id = %s"
    mycursor.execute(sql, (client_note_id,))
    mydb.commit()

    mycursor.close() # Close the database connection
    mydb.close() # Close the database connection

def login_database(username, password):
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    query = f"SELECT COUNT(*) FROM users WHERE user_name = %s AND user_password = %s"
    mycursor.execute(query, (username, password,))

    count = mycursor.fetchone()[0] # Fetch the result
    print(f"Count: {count}")

    mycursor.close()
    mydb.close()

    return count # If count is greater than 0, the user exists in the database

def check_user_database(username):
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    query = f"SELECT COUNT(*) FROM users WHERE user_name = %s"
    mycursor.execute(query, (username,))

    count = mycursor.fetchone()[0] # Fetch the result
    print(f"Count: {count}")

    mycursor.close()
    mydb.close()

    return count # If count is greater than 0, the user exists in the database

def registar_database(username, password):
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    query = f"INSERT INTO users (user_name, user_password) VALUES (%s, %s)"
    mycursor.execute(query, (username, password,))
    mydb.commit()

    mycursor.close()
    mydb.close()



def handle_client(client_socket, client_address):
    try:
        print(f'[*] Accepted connection from address: {client_address[0]}:{client_address[1]}')
        run(client_socket)  # Passa também o endereço do cliente

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()

def run(client_socket):

    while True:
    
        request = client_socket.recv(4096)
        server_check = request.decode("utf-8")
        

        if server_check == '1':
            login_user(client_socket)
        elif server_check == '6':
            register_user(client_socket)
        elif server_check == '2':
            novas_notas(client_socket)
        elif server_check == '3':
            ver_notas(client_socket)
        elif server_check == '4':
            alterar_notas(client_socket)
        elif server_check == '5':
            eliminar_notas(client_socket)
        else:
            # client_socket.close()
            pass
            


# Function to send data to the client
def send_data(client_socket, data):
    json_data = json.dumps(data)
    client_socket.send(json_data.encode())

def novas_notas(client_socket):
    request = client_socket.recv(4096)
    print(f'\n[*] Received no decode: {request}')
    print(f'\n[*] Received: {request.decode("utf-8")}')

    store_database(request)


def ver_notas(client_socket):
    data_from_db = show_notes()  # Fetch data from the database
    print(f'\n[*] Data: {data_from_db}')
    send_data(client_socket, data_from_db)  # Send data to the client
    print(f'\n[*] Showing Notes...')
    

def alterar_notas(client_socket):
    data_from_db = show_notes()
    send_data(client_socket, data_from_db)

    request = client_socket.recv(4096)
    client_note_id = request.decode()
    print(f'\n[*] Received: {client_note_id}')

    data_to_client = select_notes(client_note_id)
    send_data(client_socket, data_to_client)

    modified_note = client_socket.recv(4096).decode()
    print(f"[*] Modified Note: {modified_note}\n")

    update_database(client_note_id, modified_note)
    print("Database Updated...")


def eliminar_notas(client_socket):
    data_from_db = show_notes()
    print(f'\n[*] Data: {data_from_db}')
    send_data(client_socket, data_from_db)

    request = client_socket.recv(4096)
    client_note_id = request.decode()

    delete_notes(client_note_id)
    print(f'\n[*] Received: {client_note_id}')
    print(f"[*] Note {client_note_id} deleted...")


def login_user(client_socket):
    global current_user
    tmp_msg = "check"

    username = client_socket.recv(4096).decode()
    client_socket.send(tmp_msg.encode())
    password = client_socket.recv(4096).decode()

    print(f'\n[*] Username Received: {username}')
    print(f'[*] Password Received: {password}')

    check_user = str(login_database(username, password))
    # client_socket.send(check_user.encode())

    if check_user == "1":
        current_user = username
        client_socket.send(check_user.encode())
        
    else:
        client_socket.send(check_user.encode())
        


def register_user(client_socket):
    tmp_msg = "check"
    global current_user

    username = client_socket.recv(4096).decode()
    print(f"Username: {username}")

    client_socket.send(tmp_msg.encode())

    password = client_socket.recv(4096).decode()
    print(f"Password: {password}")

    print(f'\n[*] Username Received: {username}')
    print(f'[*] Password Received: {password}')

    check_user = check_user_database(username)
    print(f"check_user: {check_user}")

    if check_user == "1":
        client_socket.send(str(check_user).encode())
    else:
        client_socket.send(str(check_user).encode())
        registar_database(username, password)
        current_user = username


    

if __name__ == "__main__":
    start_server()
