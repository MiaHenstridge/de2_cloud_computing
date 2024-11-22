# %%
from pathlib import Path

# RSA encryption modules from pycryptodome library
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

# %%
# Define paths for our key files
PROJECT_FOLDER = Path(__file__).parent.parent
PRIVATE_KEY_FILE = PROJECT_FOLDER / "ceu_key"  # Contains the private key
# %%
# Make sure our key files exist before proceeding
assert Path.exists(PRIVATE_KEY_FILE)

# %%
# Load the public key to decrypt the message
with open(PRIVATE_KEY_FILE, "r", encoding="utf-8") as key_file:
    private_key = RSA.import_key(key_file.read())

# %%
ENCRYPTED_MESSAGE_FILE = PROJECT_FOLDER / "encrypted_message_assignment1.bin"
# Read the encrypted message from file
with open(ENCRYPTED_MESSAGE_FILE, "rb") as f:
    encrypted_message_from_file = f.read()

# %%
# Create a cipher object using the private key for decryption
private_key_cipher = PKCS1_OAEP.new(private_key)

# Decrypt the message using the private key
decrypted_message = private_key_cipher.decrypt(encrypted_message_from_file)
print(f"Decrypted message: {decrypted_message.decode('utf-8')}")

# %%
