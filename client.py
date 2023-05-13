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
