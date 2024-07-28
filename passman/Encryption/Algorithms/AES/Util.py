import base64

from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

salt_size = 8
key_size = 32


def generate_aes_key_data(password):
    if is_empty(password):
        return None
    salt = get_random_bytes(salt_size)
    key = PBKDF2(password, salt, key_size)
    return key, salt


def get_aes_key_data(password, salt):
    if is_empty(password) or is_empty(salt):
        return None
    key = PBKDF2(password, salt, key_size)
    return key


def get_encoded_bytes(text: str):
    if is_empty(text):
        return None
    return text.encode('utf8')


def get_decoded_string(data_bytes: bytes):
    if is_empty(data_bytes):
        return None
    return data_bytes.decode('utf8')


def bytes_to_string(data_bytes: bytes):
    if is_empty(data_bytes):
        return None
    return base64.b64encode(data_bytes).decode('utf8')


def string_to_bytes(data_string: str):
    if is_empty(data_string):
        return None
    return base64.b64decode(data_string.encode('utf8'))


def is_empty(text):
    if text is None or len(text) == 0:
        return True
    return False
