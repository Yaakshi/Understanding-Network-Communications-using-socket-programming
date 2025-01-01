import socket

# Create a socket object
c = socket.socket()

# Connect to the server
c.connect(('localhost', 1111))
print("Connected to SERVCHAT")

# Chat with the server
while True:
    # Send message to the server
    message = input("You: ")
    c.send(bytes(message,'utf-8'))

    if message.lower() == 'exit':
        print("You have left the chat.")
        break

    # Receive response from the server
    response = c.recv(1024).decode()
    if response.lower() == 'exit':
        print("Server has left the chat.")
        break
    print("Server: ",response)

# Close the connection
c.close()
