from cryptography.fernet import Fernet

# Function to generate and save a key
def generate_key():
    """SECRET!!!!"""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Function to load the key
def load_key():
    return open("secret.key", "rb").read()

# Function to encrypt a password
def encrypt_password(password):
    """You can put this one on public"""
    key = load_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Function to decrypt a password
def decrypt_password(encrypted_password):
    key = load_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password


if __name__ == "__main__":
    # Generate and save a key (only need to run this once)
    # generate_key()

    # Example usage
    # password = "pass"
    # email = "sender@email.com"
    # target = "reciever@email.com"
    # encrypted_password = encrypt_password(password)
    # encrypted_sender = encrypt_password(email)
    # encrypted_r = encrypt_password(target)
    # print(f"Encrypted password: {encrypted_password}")
    # with open("pass.bin", "wb") as f:
    #     f.write(encrypted_password)
    # open("sender.bin", "wb").write(encrypted_sender)
    # open("reciever.bin", "wb").write(encrypted_r)

    # decrypted_password = decrypt_password(encrypted_password)
    # print(f"Decrypted password: {decrypted_password}")
    pass
