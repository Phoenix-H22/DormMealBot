from cryptography.fernet import Fernet

class FileEncryption:
    def __init__(self, key_file="encryption.key"):
        self.key_file = key_file
        self.key = self.load_key()

    def generate_key(self):
        key = Fernet.generate_key()
        with open(self.key_file, "wb") as keyfile:
            keyfile.write(key)

    def load_key(self):
        try:
            with open(self.key_file, "rb") as keyfile:
                return keyfile.read()
        except FileNotFoundError:
            self.generate_key()
            return self.load_key()

    def encrypt_file(self, input_file, output_file):
        with open(input_file, "rb") as file:
            data = file.read()
        encrypted_data = Fernet(self.key).encrypt(data)
        with open(output_file, "wb") as file:
            file.write(encrypted_data)

    def decrypt_file(self, input_file, output_file):
        with open(input_file, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = Fernet(self.key).decrypt(encrypted_data)
        with open(output_file, "wb") as file:
            file.write(decrypted_data)
