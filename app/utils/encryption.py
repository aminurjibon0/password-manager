from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

# 32-byte key (can be generated dynamically or stored securely)
SECRET_KEY = os.environ.get('ENCRYPTION_KEY') or b'ThisIsASecretKey1234567890123456'
BLOCK_SIZE = AES.block_size


def pad(text):
    padding = BLOCK_SIZE - len(text.encode()) % BLOCK_SIZE
    return text + chr(padding) * padding

def unpad(text):
    padding = ord(text[-1])
    return text[:-padding]

def encrypt(plain_text):
    plain_text = pad(plain_text)
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(plain_text.encode())
    return base64.b64encode(iv + encrypted).decode('utf-8')

def decrypt(cipher_text):
    raw = base64.b64decode(cipher_text)
    iv = raw[:BLOCK_SIZE]
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(raw[BLOCK_SIZE:]).decode('utf-8')
    return unpad(decrypted)
