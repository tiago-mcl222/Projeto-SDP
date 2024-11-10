from cryptography.fernet import Fernet

#definir a ecryption key
#Fernet pode fazer isto usando generate_key() method
encryption_key = Fernet.generate_key()

#create our Fernet object
cipher_suite = Fernet(encryption_key)

#now we can convert plaintext to ciphertext
#we need to pass the byte format of plaintext with b
msg = "Hello World"
encrypted_value = cipher_suite.encrypt(b'msg')
print("Encrypted value: ", encrypted_value)

#value = b'b'gAAAAABltC7efobkUaRg9vOvthKbkPbHQEz194RBJn4IDh_d6ijY-V4p2K1BBJUF-MzH2EtHJgbaTS0XtSej1OpemfVWWnIrgQ=='

#the byte format can be removed using decode()
print("Encrypted value: ", encrypted_value.decode())

#to decrypt the encrypted value to plain text
decrypted_value = cipher_suite.decrypt(encrypted_value)

print("Dencrypted value: ", decrypted_value)

#to display in original format and remove byte format we use decode()
print("Dencrypted value: ", decrypted_value.decode())