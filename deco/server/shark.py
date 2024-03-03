import pyshark
from Crypto.Protocol.KDF import HKDF
import hashlib
import hmac
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def decrypt_tls_record(encrypted_record, session_key):
    # The first 16 bytes of the encrypted_record are the IV for TLS 1.2
    iv = encrypted_record[:16]
    encrypted_message = encrypted_record[16:]

    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted_message)
    
    return unpad(decrypted, AES.block_size)

def read_pre_master_secret(client_random):
    print("Reading pre-master secret from keylog.txt", client_random)
    with open('./keylog.txt', 'r') as file:
        for line in file:
            if line.startswith('CLIENT_RANDOM') and client_random in line:
                parts = line.strip().split(' ')
                if len(parts) == 3:
                    return bytes.fromhex(parts[2])
    return None

def derive_keys(pre_master_secret, client_random, server_random):
    # Convert client and server random values from hex to bytes
    client_random_bytes = bytes.fromhex(client_random.replace(':', ''))
    server_random_bytes = bytes.fromhex(server_random.replace(':', ''))

    # Concatenate client and server random values
    randoms = client_random_bytes + server_random_bytes

    # Use HKDF to derive the master secret
    master_secret_length = 48  # Define the length of the master secret
    master_secret = HKDF(pre_master_secret, master_secret_length, randoms + b"master secret", SHA256)
    print("Master secret:", master_secret)

    # Derive the client and server write keys using the master secret
    key_material_length = 104  # Length for two 32-byte keys and two 20-byte MAC keys
    key_material = HKDF(master_secret, key_material_length, randoms + b"key expansion", SHA256)
    print("Key material:", key_material)


    # Extract keys from the key material
    client_write_MAC_key = key_material[0:20]
    server_write_MAC_key = key_material[20:40]
    client_write_key = key_material[40:72]  # AES-256 key size is 32 bytes
    server_write_key = key_material[72:104]  # AES-256 key size is 32 bytes

    return client_write_key

def main():
    # capture = pyshark.LiveCapture(interface='lo0', bpf_filter='(tcp port 8000) and (tcp[((tcp[12] & 0xf0) >> 2)] = 22 or tcp[((tcp[12] & 0xf0) >> 2)] = 23)')
    capture = pyshark.LiveCapture(interface='lo0', bpf_filter='tcp port 8000')

    captured_packets = []
    client_random = None
    server_random = None
    client_fin_received = False
    server_fin_received = False
    client_port = 8000

    for packet in capture.sniff_continuously():
            captured_packets.append(packet)

            # count how many tls layers are in the packet
            tls_count = 0
            for layer in packet.layers:
                if layer._layer_name == 'tls':
                    tls_count += 1


            if 'TLS' in packet:
                print(f"TLS count: {tls_count}")
                try:
                    # Check for ClientHello message
                    if packet.tls.handshake_type == '1':  # Handshake Type 1 is ClientHello
                        client_random = packet.tls.handshake_random

                    # Check for ServerHello message
                    elif packet.tls.handshake_type == '2':  # Handshake Type 2 is ServerHello
                        server_random = packet.tls.handshake_random
                        print("Server random:", server_random)
                        cipher_suite = packet.tls.handshake_ciphersuite
                        print("Cipher Suite:", cipher_suite)
                except AttributeError:
                    # This block executes if handshake_type is not found
                    pass

            if any(layer.layer_name == 'tcp' for layer in packet.layers):
                tcp_layer = packet.tcp
                src_port = int(tcp_layer.srcport)
                dst_port = int(tcp_layer.dstport)
                # Extracting the flags field which is a hexadecimal representation
                flags_hex = int(tcp_layer.flags, 16)
                fin_flag_set = flags_hex & 0x01  # FIN flag is the least significant bit

                if fin_flag_set:
                    print(f"TCP FIN flag set by {'client' if src_port == client_port else 'server'}.")
                    if src_port == client_port:  # Replace client_port with the actual client port
                        client_fin_received = True
                    else:
                        server_fin_received = True

                # Check if both sides have sent FIN
                if client_fin_received and server_fin_received:
                    print("FIN flags received from both client and server, ending capture.")
                    break
    
    print("Captured a complete TLS session.")
    print("Client random:", client_random)



    if client_random and server_random:
        client_random_str = client_random.replace(':', '')
        pre_master_secret = read_pre_master_secret(client_random_str)
        print("Pre-master secret:", pre_master_secret)
        if pre_master_secret:
            client_write_key  = derive_keys(pre_master_secret, client_random, server_random)
            decrypted_messages = []
            captured_data = b''
            app_data = 0

            for packet in captured_packets:
                try:
                    for layer in packet.layers:

                        if layer._layer_name == 'tls':
                            print("TLS packet found")
                            captured_data +=  bytes.fromhex(packet.tls.app_data.replace(':', ''))
                            print('fields', packet.tls.record.all_fields)
                            print('cd', packet.tls.app_data)
                            print("Total length of data:", len(captured_data))
                            # print(packet)
                            app_data += 1
                            # # Check if the current accumulated data forms a complete TLS record
                            # decrypted_data = decrypt_tls_packet_cbc(captured_data, client_write_key)
                            decrypted_data = decrypt_tls_record(captured_data, client_write_key)
                            # print("TLS packet found2")

                            decrypted_messages.append(decrypted_data.decode('utf-8', errors='ignore'))
                            captured_data = b''  # Reset buffer after successful decryption


                except Exception as e:
                    print(f"Error processing packet: {e}")
                    # if('tls' in packet):
                    #     print('tls', packet.tls._all_fields)
                    # # print(packet)
                    continue

            with open('decrypted_messages.txt', 'w') as f:
                f.writelines(decrypted_messages)
            print("Decrypted messages saved to decrypted_messages.txt")
            print("Total app data packets:", app_data)

        else:
            print("Pre-master secret not found for the given client random.")
    else:
        print("Failed to capture a complete TLS session.")

if __name__ == "__main__":
    main()
