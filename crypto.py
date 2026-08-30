from cryptography.fernet import Fernet
import dotenv, os
import app

dotenv.load_dotenv(".env", override=True)

def encode_string(param): #fungsi encoding untuk push ke database

    key = os.getenv("encryption_key")
    f = Fernet(key.encode())
    token = f.encrypt(param.encode("utf-8"))
    token_encrypted = token.decode("utf-8")

    return token_encrypted

def decode_string(param) : #fungsi decoding untuk tampilan frontend (input tuple expected)
    listed_data = []

    if not isinstance(param, list) : #cek apakah input list, kalo tidak maka excecute jika tidak lanjut if else
        key = os.getenv("encryption_key")
        f = Fernet(key.encode())
        token = f.decrypt(param.encode("utf-8"))
        token_decrypted = token.decode("utf-8")
        return token_decrypted

    for i , item in enumerate(param) : #input list dipisah jadi per item, dan di decrypt secara rekursif
        listed_data.append(decode_string(item))
        
    return listed_data