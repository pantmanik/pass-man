from passman.Manager.EncryptionManager import get_key, generate_key
from passman.Manager.PasswordManager import get_salt, fetch_password, save_password, save_salt, remove_password

MASTER_PASS_VERIFICATION_USERNAME = 'DEFAULT_USER'
MASTER_PASS_VERIFICATION_SERVICE = 'DEFAULT_SERVICE'
MASTER_PASS_VERIFICATION_DUMMY_PASSWORD = 'DUMMY_PASSWORD'


def verify_master_password(master_password):
    salt = get_salt(MASTER_PASS_VERIFICATION_USERNAME, MASTER_PASS_VERIFICATION_SERVICE)
    if is_empty(salt):
        print('Master password not set!')
        return None
    aes_key = get_key(master_password, salt)
    res = fetch_password(MASTER_PASS_VERIFICATION_USERNAME, MASTER_PASS_VERIFICATION_SERVICE, aes_key)
    if is_empty(res):
        return False
    return True


def set_master_password(master_password):
    if is_master_password_set():
        print('Master pass is already set!')
        return
    aes_key, salt = generate_key(master_password)
    save_password(MASTER_PASS_VERIFICATION_DUMMY_PASSWORD, MASTER_PASS_VERIFICATION_USERNAME,
                  MASTER_PASS_VERIFICATION_SERVICE, aes_key)
    save_salt(salt, MASTER_PASS_VERIFICATION_USERNAME, MASTER_PASS_VERIFICATION_SERVICE)


def unset_master_password():
    remove_password(MASTER_PASS_VERIFICATION_USERNAME, MASTER_PASS_VERIFICATION_SERVICE)


def is_master_password_set():
    salt = get_salt(MASTER_PASS_VERIFICATION_USERNAME, MASTER_PASS_VERIFICATION_SERVICE)
    return not is_empty(salt)


def is_empty(data):
    if data is None or len(data) == 0:
        return True
    return False
