import base64
import binascii

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter

key_bytes = 32


def encrypt(key, raw_bytes):
    iv = get_random_bytes(AES.block_size)
    iv_as_int = int(binascii.hexlify(iv), 16)
    ctr = Counter.new(AES.block_size * 8, initial_value=iv_as_int)
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    ciphertext = aes.encrypt(raw_bytes)
    return ciphertext, iv


def decrypt(ciphertext, key, iv):
    iv_as_int = int(iv.hex(), 16)
    ctr = Counter.new(AES.block_size * 8, initial_value=iv_as_int)
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)

    # Decrypt and return the plaintext.
    plaintext = aes.decrypt(ciphertext)
    return plaintext

# if __name__ == '__main__':
#     text = "Encrypt this!"
#     password = "admin123"
#     salt_bytes = 8
#     salt = get_random_bytes(salt_bytes)
#     key = PBKDF2(password, salt, key_bytes)
#
#     cipher_text, iv = encrypt(key, text.encode('utf8'))
#     print(f"iv : {base64.b64encode(iv)}, ciphertext : {base64.b64encode(cipher_text)}")
#     plain = decrypt(cipher_text, key, iv)
#     print(f"deciphered : {plain}")
