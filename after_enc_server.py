# Client should use RSA package to generate public and private key and share the public key with server. DONE
# The server chooses a symmetric key and encrypt the symmetric key using public key of client and send it to client. DONE
# The client should decrypt and get the symmetric key. DONE
# After this, all the messages shared between client and server should be encrypted. DONE
# Sender needs to send HASH (of your choice) of the ciphertext also along with ciphertext. DONE
# # The receiver should, first, verify the HASH and then decrypt the ciphertext. DONE

import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from hashlib import sha256
from Crypto.Util.Padding import pad, unpad

# Create a socket object
s = socket.socket()

# Bind the socket to the address
s.bind(('localhost', 1111))

# Listen 1 client at a time
s.listen(1)
print("Server started")

# Accept a connection
c, addr = s.accept()
print("Client connected.")

# Receive public key from client
client_public_key = RSA.import_key(c.recv(4096))
print("Public key received from client")

# Generate a random AES symmetric key
aes_key = get_random_bytes(16)

# Encrypt the AES key with the client's public key
cipher_rsa = PKCS1_OAEP.new(client_public_key)
encrypted_aes_key = cipher_rsa.encrypt(aes_key)

# Send the encrypted AES key to the client
c.sendall(encrypted_aes_key)
print("Encrypted AES Key sent to client")

# Chat with the client
while True:
    # Receive IV, ciphertext, and hash from client
    iv = c.recv(16)  # CBC mode IV is 16 bytes
    ciphertext = c.recv(4096)
    received_hash = c.recv(32)  # SHA-256 is 32 bytes long

    # Verify integrity by calculating the hash of the received ciphertext
    calculated_hash = sha256(ciphertext).digest()
    if calculated_hash != received_hash:
        print("Message integrity compromised!")
        break

    # Decrypt the ciphertext using AES CBC mode
    aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    try:
        decrypted_message = unpad(aes_cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
    except ValueError:
        print("Decryption failed or padding is incorrect.")
        break

    # Client exit condition
    if decrypted_message.lower() == 'exit':
        print("Client has left the chat.")
        break

    print("Client:", decrypted_message)

    # Send response to the client
    message = input("You: ")

    # Encrypt the server's message using AES CBC mode
    aes_cipher = AES.new(aes_key, AES.MODE_CBC)
    iv = aes_cipher.iv
    padded_message = pad(message.encode(), AES.block_size)
    ciphertext = aes_cipher.encrypt(padded_message)
    hash_of_ciphertext = sha256(ciphertext).digest()

    # Send the IV, ciphertext, and hash
    c.sendall(iv)
    c.sendall(ciphertext)
    c.sendall(hash_of_ciphertext)

    # Server exit condition
    if message.lower() == 'exit':
        print("You have left the chat.")
        break

# Close the connection
c.close()
s.close()
