from cryptography.fernet import Fernet
from django.conf import settings
import os,json
# from .models import Configuration
# _key_file='secret.key'
# def generate_key():
#     """
#     Generates a key and save it into a file
#     """
#     key = Fernet.generate_key()
#     print(f"generated key: {key} to file {_key_file}")
#     with open(_key_file, "wb") as key_file:
#         key_file.write(key)

def load_key():
    """
    Load the previously generated key
    """
    #load configuration from db
    # conf = Configuration.objects.get(key="ENCRYPTION_KEY")

    return bytearray(settings.ENCRYPTION_KEY)#open(_key_file, "rb").read()

def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    # print(encrypted_message)
    return encrypted_message.decode('utf-8')
def decrypt_message(message):
    """
        decrypts a message
        """
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.decrypt(message.encode())
    # print(encrypted_message)
    return encrypted_message.decode('utf-8')
def write_backup(config):
    with open('config.json.bak', 'w') as f:
        f.write(json.dumps(config))

# if __name__ == "__main__":
#
#     if not  os.path.exists(_key_file):
#         generate_key()
#     if not os.path.exists('config.json'):
#         exit()
#     else:
#
#         config ={}
#         with open('config.json', 'r') as f:
#
#             config = json.loads(f.read())
#             write_backup(config)
#             for k,v in config.items():
#                 if type(v) != dict:
#                     continue
#
#                 else:
#                     print(f'processing {k} config')
#                     if 'password' in v:
#                         config[k]['password']=encrypt_message(config[k]['password']).decode('utf-8')
#             # f.write(json.dumps(config))
#         with open('config.json', 'w') as f:
#             f.write(json.dumps(config))
        # encrypt_message("encrypt this message")
        # decrypt_message('gAAAAABf1lvyRVVGq9O7xZ3mwhw49EenLXXCy5kuVRcRpgDCsFGGgYLiDqTAyp7CGerBIczXATZvc3kiN64Bpm9358JuKmvceawnEvZrgEGtoS8bXRGFeD8=')
