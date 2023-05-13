import socket
from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
import tkinter as tk

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
def send_message(input_entry):
    message = input_entry.get()
    encrypted_message = encrypt(message.encode(), key)
    client_socket.sendall(encrypted_message)
    input_entry.delete(0, tk.END)
    
def authenticate(password_entry, authenticate_button):
    global key, root
    
    password = password_entry.get()
    client_socket.sendall(password.encode())
    response = client_socket.recv(1024)
    
    
    if response == b"OK":
        password_label.destroy()
        password_entry.destroy()
        authenticate_button.destroy()
        
        input_label = tk.Label(root, text = "Enter a message:")
        input_label.pack()
        
        input_entry = tk.Entry(root)
        input_entry.pack

send_button=tk.Button(root,text="Send",command=lambda:send_message(input_entry))
send_button.pack()
key=derive_key(password.encode(),salt)
else:
    password_entry.delete(0,tk.END)
    password_entry.insert(0,"Authentication Failed")
    def client():
        global client_socket,key,password_label,root,salt
        host='127.0.0.1'
        port=1234
        client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect((host,port))
        root=tk.Tk()
        root.title("Client GUI")
        password_label=tk.Label(root,text="Enter password:")
        password_label.pack()
        password_entry=tk.Entry(root,show="*")
        password_entry.pack()
        authenticate_button=tk.Button(root,text="Authenticate",command=lambda:authenticate(password_entry,authenticate_button))
        authenticate_button.pack()
        salt=client_socket.recv(16)
        root.mainloop()
        client_socket.close()
        client()
