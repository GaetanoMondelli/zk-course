import pyshark
from Crypto.Protocol.KDF import HKDF
from Crypto.Cipher import AES
import time
import hashlib

def derive_keys(pre_master_secret, client_random, server_random):
    # Concatenate client and server random values
    randoms = client_random + server_random
    
    # Use HKDF to derive the master secret
    master_secret = HKDF(pre_master_secret, 48, randoms + b"master secret", hashlib.sha256)

    # Derive the client and server write keys using the master secret
    client_write_key = HKDF(master_secret, 16, randoms + b"client write key", hashlib.sha256)
    server_write_key = HKDF(master_secret, 16, randoms + b"server write key", hashlib.sha256)

    return client_write_key, server_write_key

def decrypt_tls_packet(encrypted_data, session_key, iv):
    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    return cipher.decrypt(encrypted_data)

def main():
    # Capture packets on the eth0 interface
    capture = pyshark.LiveCapture(interface='lo0', bpf_filter='(tcp port 8000) and (tcp[((tcp[12] & 0xf0) >> 2)] = 22 or tcp[((tcp[12] & 0xf0) >> 2)] = 23)')

    # Capture TLS packets until a complete session is captured
    complete_session_captured = False
    captured_packets = []
    start_time = time.time()

    for packet in capture.sniff_continuously():
        print('captured', len(captured_packets))
        # Check if the packet contains TLS laye
        
        if packet.tcp.flags_fin == '1':
            print("Connection closed.")
            break

        if 'TLS' in packet:
            # print all the keys in the packet object

            # Check if the TLS layer contains necessary fields
            print('+1', packet['TLS'])
            try:
                if all(field in packet['TLS'] for field in ['pre_master_secret', 'Random']):
                    captured_packets.append(packet)

                    # Set complete_session_captured to True if a complete TLS session is captured
                    complete_session_captured = True

                    # Break the loop if a complete session is captured
                    break
                else:
                    print("Incomplete TLS session captured. Keep capturing...")
            except Exception as e:
                print(e)
                pass
    
    print("Captured packets:", len(captured_packets))
    
    # Derive session keys if a complete session is captured
    if complete_session_captured:
        pre_master_secret = bytes.fromhex(packet['TLS']['pre_master_secret'])
        client_random = bytes.fromhex(packet['TLS']['Random'].split(',')[0])
        server_random = bytes.fromhex(packet['TLS']['Random'].split(',')[1])

        client_write_key, server_write_key = derive_keys(pre_master_secret, client_random, server_random)

        # Decrypt and store packets
        decrypted_messages = []

        for packet in captured_packets:
            if 'TLS' in packet and 'Application Data' in packet['TLS']:
                encrypted_data = bytes.fromhex(packet['TLS']['Application Data'].replace(':', ''))
                iv = bytes.fromhex(packet['TLS']['TLS Record Layer'].iv)
                decrypted_data = decrypt_tls_packet(encrypted_data, client_write_key, iv)
                decrypted_messages.append(decrypted_data.decode('utf-8', errors='ignore'))

        # Save decrypted messages to a file
        with open('decrypted_messages.txt', 'w') as f:
            f.writelines(decrypted_messages)

        print("Decrypted messages saved to decrypted_messages.txt")

    else:
        print("Failed to capture a complete TLS session.")

if __name__ == "__main__":
    main()
