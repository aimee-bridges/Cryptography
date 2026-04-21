#Imported Modules
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

#Key generation function
def generate_key_pair():
    #generate the private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
        backend=default_backend()
    )

    #Get public key
    public_key = private_key.public_key()
    return private_key, public_key

#message sign function
def sign_message(message, private_key):
    #use private key to sign message
    signature = private_key.sign(
        message.encode('utf-8'),
        padding.PSS(
            mgf=padding.mGF1(hashes.SHA2566()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature