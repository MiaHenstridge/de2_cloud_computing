#%%
from pathlib import Path
# RSA encryption modules from pycryptodome library
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

#%%
# Define paths for our key files
PROJECT_FOLDER = Path(__file__).parent.parent
PRIVATE_KEY_FILE = PROJECT_FOLDER / "my_keypair_assignemt_1"  # Contains the private key
PUBLIC_KEY_FILE = PROJECT_FOLDER / "my_keypair_assignemt_1.pub"  # Contains the public key
# %%
# Make sure our key files exist before proceeding
assert Path.exists(PRIVATE_KEY_FILE)
assert Path.exists(PUBLIC_KEY_FILE)
# %%
# Load the private key to encrypt the message
with open(PRIVATE_KEY_FILE, 'r', encoding='utf-8') as key_file:
    private_key = RSA.import_key(key_file.read())
# %%
# message to be encrypted
short_secret_message = "Hello World!".encode('utf-8')
# %%
# Create a cipher object using the private key for encryption
private_key_cipher = PKCS1_OAEP.new(private_key)
# %%
# Encrypt our message - only someone with the public key can decrypt it
encrypted_message = private_key_cipher.encrypt(short_secret_message)
print(f"Encrypted message:")
print(encrypted_message)
# %%
# Save the encrypted message to a file
ENCRYPTED_MESSAGE_FILE = PROJECT_FOLDER / "encrypted_message_assignment1.bin"
with open(ENCRYPTED_MESSAGE_FILE, "wb") as f:
    f.write(encrypted_message)
# %%
