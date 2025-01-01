Write a socket program for client server interaction.

- It should be a two-way interaction and program should not end until either server or client types some specific word like “EXIT” or “END” etc.
- You can choose any programming language of your choice.
- You need to implement confidentiality and integrity also.
- Client should use RSA package to generate public and private key and share the public key with server.
- The server chooses a symmetric key and encrypt the symmetric key using public key of client and send it to client.
- The client should decrypt and get the symmetric key.
- You can choose any symmetric key cryptography of your choice.
- After this, all the messages shared between client and server should be encrypted.
- Sender needs to send HASH (of your choice) of the ciphertext also along with ciphertext. The receiver should, first, verify the HASH and then decrypt the ciphertext. 

Use wireshark to capture your messages before the encryption and after the encryption.
