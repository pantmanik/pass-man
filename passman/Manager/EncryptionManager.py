from passman.Encryption.Algorithms.AES.Util import *
from passman.Encryption.Algorithms.AES.GCM.Encryption import encrypt, decrypt
from passman.Encryption.Algorithms.AES.GCM.Util import *


def generate_key(password):
    key_data = generate_aes_key_data(password)
    if is_empty(key_data):
        return None
    key, salt = key_data
    return bytes_to_string(key), bytes_to_string(salt)


def get_key(password, salt):
    salt_bytes = string_to_bytes(salt)
    return bytes_to_string(get_aes_key_data(password, salt_bytes))


def encrypt_data(text, key_string: str):
    text_bytes = get_encoded_bytes(text)
    key = string_to_bytes(key_string)
    if is_empty(text) or is_empty(key):
        return None
    encrypted_data = encrypt(text_bytes, key)
    return get_decoded_string(encrypted_data_to_encoded_string(encrypted_data))


def decrypt_data(encrypted_string, key_string: str):
    key = string_to_bytes(key_string)
    encrypted_data, nonce = encoded_string_to_encrypted_data(get_encoded_bytes(encrypted_string))
    decrypted_data = decrypt(encrypted_data, key, nonce)
    return get_decoded_string(decrypted_data)
