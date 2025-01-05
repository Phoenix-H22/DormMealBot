from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

from config import Config


class FileEncryption:
    def __init__(self):
        Config.validate()  # Ensure the ENCRYPTION_KEY is loaded
        self.key = Config.ENCRYPTION_KEY

    def encrypt_file(self, input_file, output_file):
        """Encrypt the contents of the input file and save to output file."""
        with open(input_file, "rb") as file:
            data = file.read()
        encrypted_data = Fernet(self.key.encode()).encrypt(data)
        with open(output_file, "wb") as file:
            file.write(encrypted_data)
        print(f"File encrypted successfully as {output_file}")

    def decrypt_file(self, input_file, output_file):
        """Decrypt the contents of the input file and save to output file."""
        with open(input_file, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = Fernet(self.key.encode()).decrypt(encrypted_data)
        with open(output_file, "wb") as file:
            file.write(decrypted_data)
        print(f"File decrypted successfully as {output_file}")

if __name__ == "__main__":
    encryptor = FileEncryption()

    # Paths
    users_file = "users.json"
    encrypted_file = "users.json.enc"

    # Encrypt the users file
    if os.path.exists(users_file):
        encryptor.encrypt_file(users_file, encrypted_file)
        print(f"{users_file} has been encrypted to {encrypted_file}")
    else:
        print(f"Error: {users_file} not found!")