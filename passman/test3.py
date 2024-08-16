# import keyring
from passman.Manager.PasswordManager import save_password, fetch_password, save_salt, get_salt
from passman.Manager.EncryptionManager import generate_key, get_key

service_id = 'test_manik'
username = 'manik'
master_password = 'testPass'
# keyring.set_password(service_id, 'manik', 'admin123')
# keyring.set_password(service_id, 'manik', 'admin1234')
# password = keyring.get_password(service_id, 'manik')
key, salt = generate_key(master_password)
save_password('admin123', username, service_id, key)
save_salt(salt, username, service_id)
# fake_key, salt = generate_key('testPass')
saved_salt = get_salt(username, service_id)
fetched_key = get_key(master_password, saved_salt)
password = fetch_password(username, service_id, fetched_key)

print(f'password : {password}')