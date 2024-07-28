from Manager.EncryptionManager import encrypt_data, decrypt_data, generate_key, get_key


password = 'admin123'
text = 'Encrypt this too!'
key, salt = generate_key(password)
cipher_text = encrypt_data(text, key)
print(f'key : {key}, salt : {salt}, ciphertext = {cipher_text}')

decryption_key = get_key(password, salt)
print(f'decryption key : {decryption_key}')
decrypted_text = decrypt_data(cipher_text, decryption_key)
print(f'decrypted text : {decrypted_text}')