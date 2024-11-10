from cryptography.fernet import Fernet
import os

# Vai buscar a key ao ficheiro fernet
# Se existir o ficheiro fernet.key abre e lê
# Senão cria o ficheiro
def load_or_generate_key():
    try:
        with open("fernet_key.key", "rb") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("fernet_key.key", "wb") as key_file:
            key_file.write(key)
    return key

# Gere a chave
key = load_or_generate_key()

# Crie uma instância do objeto Fernet usando a chave
cipher_suite = Fernet(key)

# Encrypt
def encrypt(plain_text):
    cipher_text = cipher_suite.encrypt(plain_text)
    return cipher_text

# Decrypt
def decrypt(cipher_text):
    plain_text = cipher_suite.decrypt(cipher_text).decode()
    return plain_text