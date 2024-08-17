from passman.Manager.UserDataManager import get_data_manager, set_master_password, unset_master_password, is_master_password_set
from passman.Manager.PasswordManager import get_salt, get_password, fetch_password
from passman.Manager.EncryptionManager import get_key


SERVICE_NAME_PREFIX = 'PASS-MAN_'
SALT_PREFIX = 'SALT_'


test_master_password = 'admin123'
username = 'pantmanik2'
service_id = 'sumologic'
data_manager = get_data_manager()
set_master_password(test_master_password)
data_manager.add_entry(test_master_password, 'tempPass123', username, service_id)
encrypted_pass = get_password(SERVICE_NAME_PREFIX + service_id, username)
print(f'Encrypted pass : {encrypted_pass}')
salt = get_salt(username, service_id)
print(f'Master pass exists : {is_master_password_set()}')
aes_key = get_key(test_master_password, salt)
saved_pass = fetch_password(username, service_id, aes_key)
print(f'saved pass : {saved_pass}')
unset_master_password()
print(f'Master pass exists : {is_master_password_set()}')
