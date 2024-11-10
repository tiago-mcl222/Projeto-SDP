import socket
import sys
import json
from prompt_toolkit import prompt


#HOST = '192.168.56.1'
#HOST = socket.gethostbyname(socket.gethostname())
#PORT = 5555
primary_server = ('192.168.56.1', 5555)
backup_server = ('192.168.56.1', 5555)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect((HOST, PORT))
#print("Connected to the server")

def server_connect(server_address):
    try:
        client_socket.connect(server_address)
        print("Connected to the main server")
        return True
    except Exception as e:
        print(f"Failed to connect to the main server:{e}")
        


if server_connect(primary_server):
    server_address = primary_server
else:
    server_connect(backup_server)
    server_address = backup_server

def menu_login():
    print("─────────────────────────────")
    print("| Login |  Registar | Sair |")
    print("─────────────────────────────")

def menu():
    print("────────────────────────────────────────────────────────────────────")
    print("| Novas Notas | Ver Notas | Alterar Notas | Eliminar Notas | Sair |")
    print("────────────────────────────────────────────────────────────────────")

def menu_input():
    while True:
        menu()
        controls = input("Write here: ").split(" ")
        if controls[0] == "Novas" and controls[1] == "Notas":
            new_notes()
        elif controls[0] == "Ver" and controls[1] == "Notas":
            see_notes()
        elif controls[0] == "Eliminar" and controls[1] == "Notas":
            delete_notes()
        elif controls[0] == "Alterar" and controls[1] == "Notas":
            change_notes()
        elif controls[0] == "Sair":
            print("Exiting...")
            sys.exit()
        else:
            print("Opção Inválida.")

def login_access():
    while True:
        menu_login()
        controls = input("Write here: ").split(" ")
        if controls[0] == "Login":
            login()
        elif controls[0] == "Registar":
            registar()
        elif controls[0] == "Sair":
            print("Exiting...")
            sys.exit()
        else:
            print("Opção Inválida.")

def login():
    server_check = '1'
    client_socket.send(server_check.encode())

    print("Type your credentials\n")
    username = input("Username: ")
    password = input("Password: ")

    client_socket.send(username.encode())
    client_socket.recv(4096).decode()
    client_socket.send(password.encode())

    check_user = client_socket.recv(4096).decode()

    if check_user == "0":
        print("Access Denied. User Not Found.")
        
    else:
        print("Login Successful!")
        menu_input()

def registar():
    server_check = '6'
    client_socket.send(server_check.encode())

    print("Create an account in the system\n")
    username = input("Username: ")
    password = input("Password: ")

    client_socket.send(username.encode())
    client_socket.recv(4096).decode()
    client_socket.send(password.encode())

    check_user = client_socket.recv(4096).decode()
    print("\n")

    if check_user == "0":
        print("Registration successful.")
        menu_input()
    else:
        print("Error! The Username is not permitted! Choose a different one or type Exit.")

def new_notes():
    server_check = '2'
    client_socket.send(server_check.encode())

    print("Write your msg: \n")
    msg = input()
    print("Sending... \n")
    client_socket.send(msg.encode())

def see_notes():
    
    server_check = '3'
    client_socket.send(server_check.encode())

    # Receba dados do servidor
    data_from_server = receive_data_from_server()

    if not data_from_server:
        print("\n Não tem notas criadas.")
    else:
        # Exiba as notas para o cliente
        print("As suas Notas:")
        print('\n'.join(['. '.join(map(str, inner_list)) for inner_list in data_from_server]))
        # print(data_from_server)




def change_notes():
    server_check = '4'
    client_socket.send(server_check.encode())

    data_from_server = receive_data_from_server()

    if not data_from_server:
        print("\n Não tem notas criadas.")
    else:
        print("As suas Notas:")
        print('\n'.join(['. '.join(map(str, inner_list)) for inner_list in data_from_server]))

        print("\nSelect the number of wich note do you want to modify or type Exit to go back to menu.")
        note_id = input("Select here: ")

        if note_id == "Exit":
            menu_input()
        else:
            client_socket.send(note_id.encode())

            selected_note = receive_data_from_server()
            print("\nSelected note:")
            print(selected_note)

            modified_note = prompt(f'\nModify the note (press Enter when done): \n',
                                default = str(selected_note))

            print(f"\nModified message: {modified_note}")
            client_socket.send(modified_note.encode())

def delete_notes():
    server_check = '5'
    client_socket.send(server_check.encode())

    data_from_server = receive_data_from_server()

    if not data_from_server:
        print("\n Não tem notas criadas.")
    else:

        print("As suas Notas:")
        print('\n'.join(['. '.join(map(str, inner_list)) for inner_list in data_from_server]))

        print("\nSelect the number of wich note do you want to delete or type Exit.")
        note_id = input("Select here: ")

        if note_id == "Exit":
            menu_input()
        else:
            client_socket.send(note_id.encode())
            print(f"The note number {note_id} was deleted.")

def receive_data_from_server():
    data = client_socket.recv(1024)
    return json.loads(data)


if __name__ == "__main__":
    login_access()
    # menu_input()
