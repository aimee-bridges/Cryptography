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

#sign function — bytes accepted
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
        #public key verifys sig with bytes
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

#Create signing message — encoded bytes
message = "This message is signed!".encode('utf-8')

#Sign the message
signature = sign_message(message, private_key)
print("Signature: ", signature)

#Message sig check

#print messages
print("Correct message matches the expected message to verify the signature so should be valid, however the wrong message doesn't match so should be invalid. ")
wrong_message = "This message should not be valid".encode('utf-8')
print("Wrong message: ", wrong_message)
print("Correct message: ", message)

#check wrong message to see if working properly - should be invalid
wrong_results = verify_signature(wrong_message, signature, public_key)
if wrong_results:
    print("Wrong message should be invalid (False)")
    print("Output: ", wrong_results)
else:
    print("Wrong message should be invalid (False)")
    print("Output: ", wrong_results)

#check correct message - should be valid
correct_results = verify_signature(message, signature, public_key)
if correct_results==True:
    print("Correct message should be valid (True)")
    print("Output: ", correct_results)
else:
    print("Correct message should be valid (True)")
    print("Output: ", correct_results)

