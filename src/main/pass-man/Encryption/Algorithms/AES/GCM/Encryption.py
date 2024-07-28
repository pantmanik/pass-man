import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

IV_SIZE = 12
key_bytes = 32


# Key has to be 32 bytes
def encrypt(raw_bytes, key):
    iv = get_random_bytes(IV_SIZE)
    aes = AES.new(key, AES.MODE_GCM, iv)
    ciphertext, tag = aes.encrypt_and_digest(raw_bytes)
    return ciphertext, iv, tag


def decrypt(ciphertext_bytes, key, nonce):
    iv, tag = nonce
    aes = AES.new(key, AES.MODE_GCM, iv)
    # plaintext = ''
    try:
        plaintext = aes.decrypt_and_verify(ciphertext_bytes, tag)
        return plaintext

    except ValueError:
        print('Decryption failed!')
        return None


# if __name__ == '__main__':
#     text = "Encrypt this!"
#     password = "admin123"
#     salt_bytes = 8
#     salt = get_random_bytes(salt_bytes)
#     key = PBKDF2(password, salt, key_bytes)
#
#     cipher_text, iv, tag = encrypt(text.encode('utf8'), key)
#     print(f"iv : {base64.b64encode(iv)}, ciphertext : {base64.b64encode(cipher_text)}")
#     plain = decrypt(cipher_text, key, iv, tag)
#     print(f"GCM deciphered : {plain}")
