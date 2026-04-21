#Imported Modules
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import streamlit as st


#Digital Signature section

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

#sign function
def sign_message(message, private_key):
    #use private key to sign the encoded message
    signature = private_key.sign(
        message.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

#streamlit prescription section
#verify sig function for app
def verify_signature(message, signature, public_key):
    try:
        #verify sig with public key
        public_key.verify(
            signature,
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()

        )
        #shows signature result
        st.subheader("Signature is valid")
    except Exception as e:
        st.subheader("Signature is invalid")

#main function builds app
def main():
    #title of page
    st.title("Digital Signature SafeCare Prescription App")
    #Generate key pair & stores in sesh
    if 'private_key' not in st.session_state:
            private_key, public_key = generate_key_pair()
            st.session_state['private_key'] = private_key
            st.session_state['public_key'] = public_key


    #input message
    message = st.text_input("Enter prescription message to sign: ")

    if message:
        #Sig message shows on page
        signature = sign_message(message, private_key)
        st.subheader("Signature: ")
        st.text(signature)

        #verify signature
        verify_button = st.button("Verify Signature")
        if verify_button:
            verify_signature(message, signature, public_key)

        
if __name__ == "__main__":
    main()




