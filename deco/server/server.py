import socket
import ssl

# Load DH parameters
dh_params = 'keys/dhparam.pem'

# Create SSL context
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='keys/cert.pem', keyfile='keys/key.pem')

# Specify DH parameters and DH cipher suites
# context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA')

def start_server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.bind(address)
    sock.listen(5)
    ssl_sock = context.wrap_socket(sock, server_side=True)

    while True:
        client_socket, addr = ssl_sock.accept()
        print(f'Connection from {addr}')
        client_socket.send(b'42')
        client_socket.close()

start_server(('localhost', 8000))
