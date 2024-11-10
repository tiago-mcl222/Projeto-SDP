import socket
import json
import mysql.connector

HOST = '192.168.1.81'
PORT = 5555

#cretaing the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    
    sql_formula = f"INSERT INTO notas_teste (notas) VALUES(%s)"
    mycursor.execute(sql_formula, (request,))
    mydb.commit()

    mycursor.close() # Close the database connection
    mydb.close() # Close the database connection

def show_notes():
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    query = "SELECT * FROM notas_teste"
    mycursor.execute(query)
    result = mycursor.fetchall() # Fetch all rows

    mycursor.close() # Close the database connection
    mydb.close() # Close the database connection

    return result

def select_notes(client_note_id):
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    query = f"SELECT notas FROM notas_teste WHERE notas_id = %s"
    mycursor.execute(query, (client_note_id,))
    result = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return result

def update_database(client_note_id, modified_note):
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    sql = f"UPDATE notas_teste SET notas = %s WHERE notas_id = %s"
    mycursor.execute(sql, (modified_note, client_note_id,))
    mydb.commit()

    mycursor.close() # Close the database connection
    mydb.close() # Close the database connection

def delete_notes(client_note_id):
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    sql = f"DELETE from notas_teste WHERE notas_id = %s"
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

# Function to send data to the client
def send_data(client_socket, data):
    json_data = json.dumps(data)
    client_socket.send(json_data.encode())

# Server Function (#2 camada)
def novas_notas():    
    request = client_socket.recv(4096) #receiving msg from client
    print(f'\n[*] Received: {request.decode("utf-8")}') #printing the msg

    store_database(request)
    client_socket.close()

def ver_notas():

    data_from_db = show_notes() # Fetch data from the database
    send_data(client_socket, data_from_db) # Send data to the client
    client_socket.close() # Close the client socket

def alterar_notas():
    data_from_db = show_notes() # Fetch data from the database
    send_data(client_socket, data_from_db) # Send data to the client

    request = client_socket.recv(4096) #receiving msg from client
    client_note_id = request.decode() #"utf-8"
    print(f'\n[*] Received: {client_note_id}') #printing the msg

    data_to_client = select_notes(client_note_id) #sending the selected note
    send_data(client_socket, data_to_client)
   
    modified_note = (client_socket.recv(4096)).decode() #receiveing the modify note
    print(f"[*] Modified Note: {modified_note}\n")

    update_database(client_note_id, modified_note)
    print("Database Updated...")

    client_socket.close() # Close the client socket

def eliminar_notas():
    data_from_db = show_notes() # Fetch data from the database
    send_data(client_socket, data_from_db) # Send data to the client

    request = client_socket.recv(4096) #receiving msg from client
    client_note_id = request.decode() #"utf-8"

    delete_notes(client_note_id)
    print(f'\n[*] Received: {client_note_id}') #printing the msg
    print(f"[*] Note {client_note_id} deleted...")

    client_socket.close() # Close the client socket

def login_user():
    tmp_msg = "check" # tmp_msg so that the server does not mess the messages

    # client_socket, client_address = server_socket.accept()
    # print(f"Accepted connection from {client_address}")

    username = (client_socket.recv(4096)).decode() #receiveing the modify note
    client_socket.send(tmp_msg.encode()) # tmp_msg so that the server does not mess the messages
    password = (client_socket.recv(4096)).decode() #receiveing the modify note
    print(f'\n[*] Username Received: {username}') #printing the msg
    print(f'[*] PassWord Received: {password}') #printing the msg

    check_user = str(login_database(username, password)) 
    client_socket.send(check_user.encode())
    client_socket.close()

# Function to keep checking if the username is available, and if it is than register
def receber_username(check_user, username, password):
    tmp_msg = "check" # tmp_msg so that the server does not mess the messages

    if check_user == 0:
        registar_database(username, password)
        client_socket.send(str(check_user).encode())
        client_socket.close()
    else:
        client_socket.send(str(check_user).encode())

        client_socket.recv(4096) #receiveing the modify note
        client_socket.send(tmp_msg.encode()) # tmp_msg so that the server does not mess the messages

        username = (client_socket.recv(4096)).decode() #receiveing the modify note
        client_socket.send(tmp_msg.encode()) # tmp_msg so that the server does not mess the messages
        password = (client_socket.recv(4096)).decode() #receiveing the modify note
        
        check_user = check_user_database(username)
        receber_username(check_user, username, password)

def register_user():
    tmp_msg = "check" # tmp_msg so that the server does not mess the messages
    
    username = (client_socket.recv(4096)).decode() #receiveing the modify note
    client_socket.send(tmp_msg.encode()) # tmp_msg so that the server does not mess the messages
    password = (client_socket.recv(4096)).decode() #receiveing the modify note
    
    print(f'\n[*] Username Received: {username}') #printing the msg
    print(f'[*] PassWord Received: {password}') #printing the msg

    check_user = check_user_database(username)
    print(f"check_user: {check_user}")

    receber_username(check_user, username, password)


def server_functions():
    while True:
        client_socket, address = server_socket.accept()
        print(f'[*] Accepted connection from address: {address[0]}:{address[1]}') #info about where the connection comes from
        request = client_socket.recv(4096)
        server_check = request.decode("utf-8")
    

        if server_check == '1':
            login_user()
        elif server_check == '2':
            print("Entrou 1")
            novas_notas()
        elif server_check == '3':
            ver_notas()
        elif server_check == '4':
            alterar_notas()
        elif server_check == '5':
            eliminar_notas()

server_socket.bind((HOST, PORT)) #binding the socket
server_socket.listen() # listening
print(f'[*] Listening on HOST: {HOST} | PORT: {PORT}')
print('\nPress Ctrl-C to exit\n')


while True:
    client_socket, address = server_socket.accept()
    print(f'[*] Accepted connection from address: {address[0]}:{address[1]}') #info about where the connection comes from
    request = client_socket.recv(4096)
    server_check = request.decode("utf-8")
    
    if server_check == '1':
        login_user()
    elif server_check == '6':
        register_user()
    elif server_check == '2':
        print("Entrou 1")
        novas_notas()
    elif server_check == '3':
        ver_notas()
    elif server_check == '4':
        alterar_notas()
    elif server_check == '5':
        eliminar_notas()
    else:
        client_socket.close()
                        

