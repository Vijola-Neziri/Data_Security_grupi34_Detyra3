Visarii
----

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
