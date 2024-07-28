from Encryption.Algorithms.AES.GCM.Encryption import encrypt, decrypt
from Encryption.Algorithms.AES.GCM.Util import encoded_string_to_encrypted_data, encrypted_data_to_encoded_string
from Encryption.Algorithms.AES.Util import generate_aes_key_data, get_encoded_bytes, get_decoded_string, bytes_to_string, string_to_bytes


text = 'Encrypt this!'
password = 'admin123'
key, salt = generate_aes_key_data(password)
encoded_text_bytes = get_encoded_bytes(text)
encrypted_data = encrypt(encoded_text_bytes, key)
encrypted_data_string = encrypted_data_to_encoded_string(encrypted_data)
salt_string = bytes_to_string(salt)
print(f'encrypted string : {encrypted_data_string}, key : {key}, salt : {salt_string}')

ciphertext, nonce = encoded_string_to_encrypted_data(encrypted_data_string)
decrypted_data = decrypt(ciphertext, key, nonce)
decrypted_string = get_decoded_string(decrypted_data)
print(f'decrypted data : {decrypted_string}')
