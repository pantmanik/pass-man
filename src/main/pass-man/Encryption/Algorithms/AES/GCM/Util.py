import base64

tag_size = 16
iv_size = 12


def encrypted_data_to_encoded_string(encrypted_data):
    ciphertext, iv, tag = encrypted_data
    return base64.b64encode(iv + ciphertext + tag)


def encoded_string_to_encrypted_data(encoded_string):
    data_bytes = base64.b64decode(encoded_string)
    iv = data_bytes[:iv_size]
    tag = data_bytes[-1 * tag_size:]
    ciphertext = data_bytes[iv_size:-1 * tag_size]
    return ciphertext, (iv, tag)
