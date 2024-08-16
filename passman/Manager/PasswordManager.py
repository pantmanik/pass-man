from keyring import set_password, get_password
from passman.Manager.EncryptionManager import encrypt_data, decrypt_data

SERVICE_NAME_PREFIX = 'PASS-MAN_'
SALT_PREFIX = 'SALT_'


def save_password(password, username, service_name, aes_key):
    encrypted_password = encrypt_data(password, aes_key)
    set_password(SERVICE_NAME_PREFIX + service_name, username, encrypted_password)


def fetch_password(username, service_name, aes_key):
    encrypted_password = get_password(SERVICE_NAME_PREFIX + service_name, username)
    password = decrypt_data(encrypted_password, aes_key)
    return password


def save_salt(salt, username, service_name):
    set_password(SALT_PREFIX + service_name, username, salt)


def get_salt(username, service_name):
    return get_password(SALT_PREFIX + service_name, username)
