import socket

# Create a socket object
s = socket.socket()

# Bind the socket to the address
s.bind(('localhost', 1111))

# Listen for incoming connections (1 client at a time)
s.listen(1)
print("Server started")

# Accept a connection
c, addr = s.accept()
print("Client connected.")

# Chat with the client
while True:
    # Receive message from the client
    message = c.recv(1024).decode()
    if message.lower() == 'exit':
        print("Client has left the chat.")
        break
    print("Client: ",message)
    
    # Send response to the client
    response = input("You: ")
    c.send(bytes(response,'utf-8'))

    if response.lower() == 'exit':
        print("You have left the chat.")
        break

# Close the connection
c.close()
s.close()
