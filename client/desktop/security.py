import hashlib

def hash_password(password):
    # sha256_hash = hashlib.sha256()
    # encoded_password = sha256_hash.update(password.encode('utf-8'))
    password_hash = hashlib.sha256(password).hexdigest()
    return password_hash

def compare_hashes(password_hash1, password_hash2):
    return password_hash1 == password_hash2

if __name__ == '__main__':
    password1 = b'password'
    password2 = b'password'

    password_hash1 = hash_password(password1)
    password_hash2 = hash_password(password2)

    if compare_hashes(password_hash1, password_hash2):
        print('The passwords match')
    else:
        print('The passwords do not match')
