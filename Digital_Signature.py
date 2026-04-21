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
        key_size=2048,
        backend=default_backend()
    )

    #Get public key
    public_key = private_key.public_key()
    return private_key, public_key

#sign function — accepts raw bytes so it works for files as well as strings
def sign_message(data, private_key):
    #use private key to sign the data
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

#verify function — returns True if valid, False if not
def verify_signature(data, signature, public_key):
    try:
        #use public key to verify the signature over the same bytes
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

#Code testing

#Key pair generate
private_key, public_key = generate_key_pair()
print("Private Key: ", private_key)
print("Public Key: ", public_key)

#Create signing message — encoded to bytes because sign_message now expects bytes
message = "This message is signed!".encode('utf-8')

#Sign the message
signature = sign_message(message, private_key)
print("Signature: ", signature)


#Testing the signature validation
#tampered message uses different message but same public key = invalid
tampered_message = "This message should be invalid".encode('utf-8')
print("This message should be invalid:", verify_signature(tampered_message, signature, public_key))

#Verify signature of correct message
print("This signature should be valid:", verify_signature(message, signature, public_key))
