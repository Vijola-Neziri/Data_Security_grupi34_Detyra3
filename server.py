import socket
from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA

def encrypt(plain_text, key):
    cipher = DES.new(key, DES.MODE_CBC)
    cipher_text = cipher.encrypt(pad(plain_text, DES.block_size))
    return cipher.iv + cipher_text

def decrypt(cipher_text, key):
    iv = cipher_text[:DES.block_size]
    cipher = DES.new(key, DES.MODE_CBC, iv)
    plain_text = unpad(cipher.decrypt(cipher_text[DES.block_size:]), DES.block_size)
    return plain_text

def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=8, count=1000)

def server():
    host = '127.0.0.1'
    port = 1234

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print('Server is listening on %s:%s' % (host, port))



    client_socket, addr = server_socket.accept()
    print('Connection accepted from:', addr)

    salt = get_random_bytes(16)
    client_socket.sendall(salt)

    password = input('Enter password: ')
    key = derive_key(password.encode(), salt)

    authenticated = False


while not authenticated:
    received_password = client_socket.recv(1024).decode()
    if received_password == password:
        client_socket.sendall(b"OK")
        authenticated = True
    else:
        client_socket.sendall(b"FAIL")

while True:
    data = client_socket.recv(1024)
    if not data:
        break

    decrypted_data = decrypt(data, key)
    print('Received encrypted data:', data)
    print('Decrypted data:', decrypted_data.decode())

client_socket.close()
server_socket.close()

server()
