import os.path
import tkinter
from tkinter import filedialog

import jsonlines

from passman.Manager.EncryptionManager import get_key
from passman.Manager.MasterPasswordManager import verify_master_password
from passman.Manager.PasswordManager import get_salt, fetch_password, encrypt_and_save_password, remove_password
from passman.config import get_config

USER_DATA_FILE_NAME = 'user_data.jsonl'
USER_DATA_FILE_PATH = ''

SINGLETON_OBJECT = None


def get_work_directory_from_user():
    tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
    return filedialog.askdirectory()


def is_empty(data):
    if data is None or len(data) == 0:
        return True
    return False


def add_user_data_in_file(username, service_id):
    data = {'serviceId': service_id, 'username': username}
    with jsonlines.open(USER_DATA_FILE_PATH, mode='a') as appender:
        appender.write(data)


def delete_user_data_from_file(username, service_id):
    final_data = []
    found = False
    with jsonlines.open(USER_DATA_FILE_PATH, mode='r') as reader:
        for entry in reader.iter(type=dict, skip_invalid=True):
            file_service_id = entry.get('serviceId')
            file_username = entry.get('username')
            if file_username == username and file_service_id == service_id:
                found = True
                continue
            final_data.append(entry)
    if not found:
        print(f'Could not find the entry serviceId : {service_id}, username : {username} in file!')
        return
    with jsonlines.open(USER_DATA_FILE_PATH, mode='w') as writer:
        writer.write_all(final_data)
    print(f'Deleted entry serviceId : {service_id}, username : {username} in file!')


class UserDataManager:
    passwords = None
    userdata = None

    def __init__(self):
        global USER_DATA_FILE_PATH
        user_work_dir = get_config().work_dir
        print(f'internal dir : {user_work_dir}')
        if is_empty(user_work_dir):
            user_work_dir = get_work_directory_from_user()
        data_file_path = os.path.join(user_work_dir, USER_DATA_FILE_NAME)
        if not os.path.isfile(data_file_path):
            with open(data_file_path, 'w'):
                pass
        USER_DATA_FILE_PATH = data_file_path
        self.__init_user_data()

    def __init_user_data(self):
        with jsonlines.open(USER_DATA_FILE_PATH, mode='r') as reader:
            for entry in reader.iter(type=dict, skip_invalid=True):
                service_id = entry.get('serviceId')
                username = entry.get('username')
                if is_empty(service_id) or is_empty(username):
                    print(f"Record error. Record : {entry}")
                    continue
                self.__add_user_data_in_mem(username, service_id)

    def __add_user_data_in_file_and_mem(self, username, service_id):
        is_new_user = self.__add_user_data_in_mem(username, service_id)
        if is_new_user:
            add_user_data_in_file(username, service_id)

    def __add_user_data_in_mem(self, username, service_id):
        if is_empty(self.userdata):
            self.userdata = dict({})
        if is_empty(self.userdata.get(service_id)):
            self.userdata[service_id] = set({})
        if username in self.userdata[service_id]:
            print('Username already exists!')
            return False
        self.userdata[service_id].add(username)
        return True

    def __delete_user_data_from_file_and_mem(self, username, service_id):
        delete_user_data_from_file(username, service_id)
        self.__delete_user_data_from_mem(username, service_id)

    def __delete_user_data_from_mem(self, username, service_id):
        if is_empty(self.userdata):
            print('User data is empty!')
            return
        if is_empty(self.userdata.get(service_id)):
            print(f'No data for given service id : {service_id}')
            return
        if username not in self.userdata[service_id]:
            print(f'Username : {username} not found in service : {service_id}')
            return
        self.userdata[service_id].remove(username)

    def __fetch_and_cache_password(self, master_password, username, service_id):
        salt = get_salt(username, service_id)
        aes_key = get_key(master_password, salt)
        password = fetch_password(username, service_id, aes_key)
        self.__cache_password(password, username, service_id)
        return password

    def __cache_password(self, password, username, service_id):
        if is_empty(self.passwords):
            self.passwords = dict({})
        if is_empty(self.passwords.get(service_id)):
            self.passwords[service_id] = dict({})
        self.passwords[service_id][username] = password

    def cache_passwords(self, master_password):
        master_password_verification = verify_master_password(master_password)
        if master_password_verification is None:
            print('Master pass is not set!')
            return
        if not master_password_verification:
            print('Incorrect Master Password!')
            return
        with jsonlines.open(USER_DATA_FILE_PATH, mode='r') as reader:
            for entry in reader.iter(type=dict, skip_invalid=True):
                service_id = entry.get('serviceId')
                username = entry.get('username')
                if is_empty(service_id) or is_empty(username):
                    print(f"Record error. Record : {entry}")
                    continue
                password = self.__fetch_and_cache_password(master_password, username, service_id)
                if password is None:
                    print('Incorrect master password given, aborting the operation!')
                # We will reset the encryption on password once we cache it
                encrypt_and_save_password(master_password, password, username, service_id)

    def reset_cache(self):
        self.passwords = None

    def add_entry(self, master_password, password, username, service_id):
        master_password_verification = verify_master_password(master_password)
        if master_password_verification is None:
            print('Master pass is not set!')
            return
        if not master_password_verification:
            print('Incorrect Master Password!')
            return
        encrypt_and_save_password(master_password, password, username, service_id)
        self.__cache_password(password, username, service_id)
        self.__add_user_data_in_file_and_mem(username, service_id)

    def remove_entry(self, username, service_id):
        self.__delete_user_data_from_file_and_mem(username, service_id)
        remove_password(username, service_id)


def get_data_manager():
    global SINGLETON_OBJECT
    if SINGLETON_OBJECT is None:
        print('Initializing UserDataManager.')
        SINGLETON_OBJECT = UserDataManager()
    return SINGLETON_OBJECT
