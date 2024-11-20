#%%
from pathlib import Path
# RSA encryption modules from pycryptodome library
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

#%%
# Define paths for our key files
PROJECT_FOLDER = Path(__file__).parent.parent
PRIVATE_KEY_FILE = PROJECT_FOLDER / "my_keypair_assignment_1"  # Contains the private key
PUBLIC_KEY_FILE = PROJECT_FOLDER / "my_keypair_assignment_1.pub"  # Contains the public key
# %%
# Make sure our key files exist before proceeding
assert Path.exists(PRIVATE_KEY_FILE)
assert Path.exists(PUBLIC_KEY_FILE)
# %%
# Load the private key to encrypt the message
with open(PRIVATE_KEY_FILE, 'r', encoding='utf-8') as key_file:
    private_key = RSA.import_key(key_file.read())