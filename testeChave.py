import random
import string

chars = " " + string.punctuation + string.digits + string.ascii_letters
chars = list(chars)
key = chars.copy()

random.shuffle(key)

# print(f"chars: {chars}")
# print(f"key: {key}")

#Encrypt
def encrypt(plain_text):
    cipher_text = ""

    for letter in plain_text:
        index = chars.index(letter)
        cipher_text += key[index]
    
    return cipher_text


#Decrypt
def decrypt(cipher_text): 
    plain_text = ""

    for letter in cipher_text:
        index = key.index(letter)
        plain_text += chars[index]
    
    return plain_text

# def decrypt(cipher_text):
#     plain_text = ""

#     for letter in cipher_text:
#         try:
#             index = key.index(letter)
#             plain_text += chars[index]
#         except ValueError:
#             # Se o caractere não for encontrado em 'key', apenas o acrescente ao texto plano
#             plain_text += letter
    
#     return plain_text