# Client should use RSA package to generate public and private key and share the public key with server. DONE
# The server chooses a symmetric key and encrypt the symmetric key using public key of client and send it to client. DONE
# The client should decrypt and get the symmetric key. DONE
# After this, all the messages shared between client and server should be encrypted. DONE
# Sender needs to send HASH (of your choice) of the ciphertext also along with ciphertext. DONE
# The receiver should, first, verify the HASH and then decrypt the ciphertext. DONE

import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256

# Create a socket object
c = socket.socket()

# Connect to the server
c.connect(('localhost', 1111))
print("Connected to SERVCHAT")

# Generate RSA key pair (public and private keys)
private_key = RSA.generate(2048)
public_key = private_key.publickey().export_key()

# Send public key to the server
c.sendall(public_key)
print("Public Key sent to server")

# Receive encrypted AES key from server
encrypted_aes_key = c.recv(4096)

# Decrypt AES key using the client's private RSA key
cipher_rsa = PKCS1_OAEP.new(private_key)
aes_key = cipher_rsa.decrypt(encrypted_aes_key)
print("AES Key decrypted")

# Chat with the server
while True:
    # Client sends a message to the server
    message = input("You: ")

    # Encrypt the message using AES CBC mode
    aes_cipher = AES.new(aes_key, AES.MODE_CBC)
    iv = aes_cipher.iv
    padded_message = pad(message.encode(), AES.block_size)
    ciphertext = aes_cipher.encrypt(padded_message)
    hash_of_ciphertext = sha256(ciphertext).digest()

    # Send the encrypted_IV, ciphertext, and hash to the server
    c.sendall(iv)
    c.sendall(ciphertext)
    c.sendall(hash_of_ciphertext)

    # Client exit condition
    if message.lower() == 'exit':
        print("You have left the chat.")
        break

    # Receive IV, ciphertext, and hash from server
    iv = c.recv(16)  # CBC mode IV is 16 bytes
    ciphertext = c.recv(4096)
    received_hash = c.recv(32)

    # Verify integrity by calculating the hash of the received ciphertext
    calculated_hash = sha256(ciphertext).digest()
    if calculated_hash != received_hash:
        print("Message integrity compromised!")
        break

    # Decrypt the server's message using AES CBC mode
    aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    try:
        decrypted_message = unpad(aes_cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
    except ValueError:
        print("Decryption failed or padding is incorrect.")
        break

    # Server exit condition
    if decrypted_message.lower() == 'exit':
        print("Server has left the chat.")
        break

    print("Server: ", decrypted_message)

# Close the connection
c.close()
