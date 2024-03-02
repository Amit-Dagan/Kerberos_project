import base64
import binascii
import hashlib
import socket
import struct
import uuid
from hashlib import sha256
import datetime
import os
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

VERSION = 24
DEFULT_PORT = 1256
PORT_FILE = 'port.info'
MSG_SERVER_FILE = 'msg.info'
CLIENTS_FILE = 'clients'

HEADER_FORMAT = '16sBHI'
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
clients_name_list = []
clients_dict = {}

def main():
    
    clients_dict = load_clients_dict()
    load_clients_name_list()
    print(clients_name_list)
    port = read_server_port()
    msg_servers = load_message_server_details()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((socket.gethostname(), port))
        server_socket.listen()
        print(f"Server listening on port {port}...")
        
        while True:

            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            client_data = client_socket.recv(1024) 

            client_id, version, code, payload_size = struct.unpack(HEADER_FORMAT, client_data[:HEADER_SIZE])
            print('handeling id: ', client_id)
            if(version != VERSION):
                #TODO check if works
                continue

            if(len(client_data[HEADER_SIZE:]) != payload_size):
                print(f"len of client_data[HEADER_SIZE:] = {len(client_data[HEADER_SIZE:])} ")
                print(f"len of payload_size = {payload_size}")
                print('not the same size')
                #TODO check if works
                continue


            match code:
                case 1024:
                    user_sign_up(client_data[HEADER_SIZE:], client_socket)
                case 1025:
                    server_sign_up()
                case 1026:
                    get_servers()
                case 1027:
                    get_key(client_id, client_data[HEADER_SIZE:], client_socket)

            client_socket.close



def user_sign_up(payload, client_socket):
    print('sign up')

    payload_format = '255s255s'
    name, password_hash = struct.unpack(payload_format, payload)
    name = name.rstrip(b'\x00').decode('utf-8')
    password_hash = password_hash.rstrip(b'\x00').decode('utf-8')
    print(password_hash, name)
    print(f'name is {name} \n {clients_name_list}')
    if (name not in clients_name_list):
        try:
            with open(CLIENTS_FILE, 'a') as clients_file:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                id = get_random_bytes(16)
                while(id in clients_dict):
                    id = get_random_bytes(16)

                id_hex = binascii.hexlify(id).decode()
                clients_file.write(f'{id_hex}:{name}:{password_hash}:{current_time}\n')
                clients_dict[id] =  password_hash
                clients_name_list.append(name)
                response_code = 1600
                data = struct.pack(f'BHI16s', VERSION, response_code, 16, id)
                client_socket.sendall(data)
                return

        except Exception as e:
            print(e)
    else:
        print('1601')
    response_code = 1601
    data = struct.pack(f'BHI', VERSION, response_code, 0)
    client_socket.sendall(data)
    

def server_sign_up():
    print('sign up')


def get_key(client_id, payload, client_socket):
    

    payload_format = '16s8s'
    msg_server_id, nonce = struct.unpack(payload_format, payload)

    msg_server_key = get_random_bytes(32)
    password_hash = hashlib.sha256('1234'.encode('utf-8')).digest()
    client_key = password_hash
    code = 1027

    encrypted_key_headers = '16s16s32s'
    ticket_headers = 'B16s16s8s16s32s8s'
    data_headers = f'16s{struct.calcsize(encrypted_key_headers)}s{struct.calcsize(ticket_headers)}s'


    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode()
    aes_key = get_random_bytes(32)

    print(data_headers)

    client_cipher = AES.new(client_key, AES.MODE_CBC)
    encrypted_nonce = client_cipher.encrypt(pad(nonce, AES.block_size))
    user_encrypted_key = client_cipher.encrypt(pad(aes_key, AES.block_size))
    

    client_iv = client_cipher.iv

    msg_cipher = AES.new(msg_server_key, AES.MODE_CBC)
    msg_encrypted_key = msg_cipher.encrypt(pad(aes_key, AES.block_size))
    expiration_time = msg_cipher.encrypt(pad(current_time, AES.block_size))

    ticket_iv = msg_cipher.iv
    msg_encrypted_key = aes_key

    encrypted_key = struct.pack(encrypted_key_headers, client_iv, encrypted_nonce, user_encrypted_key)
    ticket = struct.pack(ticket_headers, 24, client_id, msg_server_id, current_time, ticket_iv, msg_encrypted_key, current_time)
    data = struct.pack(data_headers, client_id ,encrypted_key, ticket)
    print(client_id, '\n', data)

    print('get key')
    client_socket.sendall(data)

    return


def get_servers():
    print('get servers list')




def load_clients_name_list():
    try:
        with open(CLIENTS_FILE, 'r') as clients_file:
            clients = clients_file.readlines()
            for client in clients:
                name = client.split(':')[1].strip()
                clients_name_list.append(name)
            clients_file.close
    except FileNotFoundError:
        with open(CLIENTS_FILE, 'w') as clients_file:
            clients_file.close


    except Exception as e:
        print (e)


def load_clients_dict():
    client_dict = {}
    try:
        with open(CLIENTS_FILE, 'r') as clients_file:
            clients = clients_file.readlines()
            for client in clients:
                client_data = client.split(':')
                client_id = client_data[0].strip()
                password_hash = client_data[2].strip()
                client_dict[client_id] = password_hash
    except FileNotFoundError:
        with open(CLIENTS_FILE, 'w') as clients_file:
            clients_file.close()
    except Exception as e:
        print(e)

    return client_dict






def read_server_port():
    try:
        port_file_path = os.path.join(os.path.dirname(__file__), 'port.info')
        with open(port_file_path, 'r') as file:
            port = int(file.read().strip())
            print(f"Using port {port} from {PORT_FILE} file.")
            return port
    except Exception as e:
        print(f"Warning: {PORT_FILE} file not found or invalid. Using default port {DEFULT_PORT}. Error: {e}")
        return DEFULT_PORT

    
def load_message_server_details():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'msg.info')
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) < 4:
                raise ValueError("Invalid msg.info format")
            ip_address, port = lines[0].strip().split(':')
            server_details = {
                'ip_address': ip_address,
                'port': int(port),
                'server_name': lines[1].strip(),
                'unique_identifier': lines[2].strip(),
                'symmetric_key_base64': lines[3].strip()
            }

            # Printing the loaded message server details
            print("Loaded message server details from msg.info:")
            # for key, value in server_details.items():
            #     print(f"{key}: {value}")

            return server_details
    
    except FileNotFoundError:
        print("msg.info file not found.")
        return None
    except ValueError as e:
        print(f"Error reading msg.info file: {e}")
        return None
    except Exception as e:
        print(f"Failed to load msg.info: {e}")
        return None









if __name__ == "__main__":
    main()