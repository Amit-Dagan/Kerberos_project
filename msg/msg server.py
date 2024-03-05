import os
import socket
import struct
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

VERSION = 24  # Assuming the same version as in your authentication server
HEADER_FORMAT = '16sBHI'
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

def load_server_details():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'msg.info')
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
            ip_address, port = lines[0].split(':')
            symmetric_key_base64 = lines[3]
            symmetric_key = symmetric_key_base64.encode('utf-8')
            return ip_address, int(port), symmetric_key
    except Exception as e:
        print(f"Error loading server details: {e}")
        return None



def decrypt_authenticator(encrypted_authenticator, key):
    # Assuming the Authenticator IV is the first 16 bytes of the encrypted authenticator
    iv = encrypted_authenticator[:16]
    encrypted_data = encrypted_authenticator[16:]

    # Initialize AES cipher in CBC mode with the given key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the data and unpad it
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    # Extract the fields from the decrypted Authenticator data
    version, client_id, server_id, creation_time = struct.unpack('!B16s16s8s', decrypted_data)

    # Return the extracted fields or the entire decrypted data as needed
    return {
        'version': version,
        'client_id': client_id,
        'server_id': server_id,
        'creation_time': creation_time
    }


def decrypt_ticket(encrypted_ticket, key):
    # Extract the Ticket IV, which is located after Version, Client ID, Server ID, Creation Time, and Expiration Time
    # Totaling 1 + 16 + 16 + 8 + 8 = 49 bytes before the Ticket IV
    ticket_iv = encrypted_ticket[49:65]  # The Ticket IV is 16 bytes long

    # The Encrypted AES Key and potentially other encrypted content follow the Ticket IV
    encrypted_data = encrypted_ticket[65:]

    # Initialize AES cipher in CBC mode with the given key and IV
    cipher = AES.new(key, AES.MODE_CBC, ticket_iv)

    # Decrypt the data and unpad it
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    # Since the AES Key is encrypted and its structure might depend on the encryption scheme,
    # further parsing of decrypted_data might be necessary to extract the AES Key and any other data

    # Return the decrypted AES Key and any other information needed
    return decrypted_data  # Modify this return statement based on how you need to use the decrypted data

def handle_client(client_socket, server_key):
    try:
        client_data = client_socket.recv(1024)
        if not client_data:
            return
        print(client_data)
        print('\n')
        ticket_headers = 'B16s16s8s16s32s8s'
        version, client_id, msg_server_id, current_time, ticket_iv, msg_encrypted_key, current_time = struct.unpack(ticket_headers, client_data)
        print(version, client_id, msg_server_id, current_time, ticket_iv, msg_encrypted_key, current_time)

        if version != VERSION:
            print("Protocol version mismatch.")
            return
        #change to code
        if version == 1028:  # Assuming 1028 is the code for a specific operation, e.g., sending a message
            # decrypted_payload = decrypt_message(payload, server_key)
            # Further processing of decrypted_payload as per your application logic

            # print("Decrypted message:", decrypted_payload.decode('utf-8'))
            print('asd')
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def main():
    server_details = load_server_details()
    print(server_details)
    if server_details is None:
        return

    ip_address, port, server_key = server_details

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((ip_address, port))
        server_socket.listen()
        print(f"Message Server listening on {ip_address}:{port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            handle_client(client_socket, server_key)

if __name__ == "__main__":
    main()


users = {
    'jack': '12312314wadfas',
    'amit': 'asdasdfhefhi314'
}