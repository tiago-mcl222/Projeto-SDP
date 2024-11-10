import socket
import sys
import json
from prompt_toolkit import prompt



HOST = '192.168.1.81'
PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT)) #connection
print("Connected to the server")


def menu_login():
    print("─────────────────────────────")
    print(f"| Login |  Registar | Sair |")
    print("─────────────────────────────")

def menu():
    print("────────────────────────────────────────────────────────────────────")
    print(f"| Novas Notas | Ver Notas | Eliminar Notas | Alterar Notas | Sair |")
    print("────────────────────────────────────────────────────────────────────")

def menu_input():
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
        print("Tente novamente ou selecione Sair.")
        menu()
        menu_input()


def login_access():
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
        print("Tente novamente ou selecione Sair.")
        menu_login()
        login_access()
       
def login():
    server_check = '1'
    client_socket.send(server_check.encode())

    print("Type your credentials\n")
    username = input("Username: ")
    password = input("Password: ")

    client_socket.send(username.encode())
    client_socket.recv(4096).decode() # tmp_msg so that the server does not mess the messages
    client_socket.send(password.encode()) # encoding the msg to be send

    check_user = client_socket.recv(4096).decode()

    if check_user == "0":
        client_socket.close()
        print("Acces Denied. User Not Found.")
        
    else:
        print("Login Succeful!")
        menu_input()
  

def registar():
    server_check = '6'
    client_socket.send(server_check.encode())

    print("Create an account in the system\n")
    username = input("Username: ")
    password = input("Password: ")
    
    # # Client setup
    # client_socket.connect((HOST, PORT)) #connection

    client_socket.send(username.encode())
    client_socket.recv(4096).decode() # tmp_msg so that the server does not mess the messages
    client_socket.send(password.encode()) # encoding the msg to be send

    check_user = client_socket.recv(4096).decode()
    print("\n")

    if check_user == "0":
        print("Registration successful.")
        menu_input() 
    else:
        print("Error! The Username is not permited! Chose a diferent one or type Exit.")
        registar()


#while True:
def new_notes():
    server_check = '2'
    client_socket.send(server_check.encode())

    print("Write your msg: \n")
    # while True:  tem a ver com response em baixo   
    msg = input() #msg => menssage send
    print("Sending... \n")
    client_socket.send(msg.encode()) # encoding the msg to be send

    # Close the client socket
    # client_socket.close()

def see_notes():
    server_check = '3'
    client_socket.send(server_check.encode())

    # Receive data from the server
    data_from_server = receive_data_from_server()

    #Show notes to client
    print("As suas Notas:") #Data received from server
    print('\n'.join(['. '.join(map(str, inner_list)) for inner_list in data_from_server]))

    # Close the client socket
    # client_socket.close()
    # main.menu_input()


def change_notes():
    server_check = '4'
    client_socket.send(server_check.encode())

    # Receive data from the server
    data_from_server = receive_data_from_server()

    #Show notes to client
    print("As suas Notas:") #Data received from server
    print('\n'.join(['. '.join(map(str, inner_list)) for inner_list in data_from_server]))

    print("\nSelect the number of wich note do you want to modify or type Exit.")
    note_id = input("Select here: ")

    if note_id == "Exit":
        # client_socket.close() # Close the client socket
        pass
    else:
        client_socket.send(note_id.encode()) # encoding the msg to be send

        selected_note = receive_data_from_server() #receiving the note
        print("\nSelected note:")
        print('\n'.join(['. '.join(map(str, element)) for element in selected_note]))

        # prompt_toolkit allows editing
        modified_note = prompt(f'\nModify the note (press Enter when done): \n',
                            default = str(' '.join(['. '.join(map(str, element)) for element in selected_note])))

        print(f"\nModified message: {modified_note}")
        client_socket.send(modified_note.encode()) # encoding the msg to be send
        # Close the client socket
        # client_socket.close()

def delete_notes():
    server_check = '5'
    client_socket.send(server_check.encode())

    # Receive data from the server
    data_from_server = receive_data_from_server()

    #Show notes to client
    print("As suas Notas:")
    print('\n'.join(['. '.join(map(str, inner_list)) for inner_list in data_from_server]))

    print("\nSelect the number of wich note do you want to delete or type Exit.")
    note_id = input("Select here: ")

    if note_id == "Exit":
        # client_socket.close() # Close the client socket
        pass
    else:
        client_socket.send(note_id.encode()) # encoding the msg to be send
        print(f"The note number {note_id} was deleted.")
        # Close the client socket
        # client_socket.close()
        

def receive_data_from_server():
    data = client_socket.recv(1024).decode()
    return json.loads(data)




def main():
    login_access()
    # menu_input()

if __name__ == "__main__":
    main()