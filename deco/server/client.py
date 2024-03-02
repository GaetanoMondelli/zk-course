import os
import socket
import ssl
# import sslkeylog

# Create a regular socket

# sslkeylog.set_keylog('./sslkeys_google.log')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create SSL context
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

# Specify DH cipher suites
# context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA')

# Set other SSL context options
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Wrap the socket with SSL
wrappedSocket = context.wrap_socket(sock, server_hostname='localhost')

print(os.environ['SSLKEYLOGFILE'])

# Connect to the server
wrappedSocket.connect(('localhost', 8000))

# Receive data from the server
received_data = wrappedSocket.recv(1024)
print("Received:", received_data)

# Close the connection
wrappedSocket.close()
