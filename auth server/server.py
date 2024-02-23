import base64
import binascii
import socket
import struct
import uuid
from hashlib import sha256
import datetime
import os
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

VERSION = 24
DEFULT_PORT = 1256
PORT_FILE = 'port.info'
MSG_SERVER_FILE = 'msg.info'
CLIENTS_FILE = 'clients'

HEADER_FORMAT = '16sBHI'
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


def main():
    print('main')
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
                        get_key(client_data[HEADER_SIZE:], client_socket)

                client_socket.close()




def user_sign_up(payload, client_socket):
    print('sign up')

    payload_format = '255s255s'
    name, password_hash = struct.unpack(payload_format, payload)
    name = name.rstrip(b'\x00').decode('utf-8')
    password_hash = password_hash.rstrip(b'\x00').decode('utf-8')
    print(password_hash, name)
    clients_name_list = load_clients_id_list()

    if (name not in clients_name_list):
        
        try:
            with open(CLIENTS_FILE, 'a') as clients_file:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                id = get_random_bytes(16)
                id_hex = binascii.hexlify(id).decode()
                clients_file.write(f'{id_hex}:{name}:{password_hash}:{current_time}\n')
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

def get_key(payload, client_socket):
    
    payload_format = '16s8s'
    msg_server_id, nounce = struct.unpack(payload_format, payload)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg_server_key = get_random_bytes(32)
    key = get_random_bytes(16)


    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes1 = cipher.encrypt(pad(data, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct1 = b64encode(ct_bytes1).decode('utf-8')


    encrypted_key  = struct.pack(f'16s3s32s', iv, )




    print('get key')


def get_servers():
    print('get servers list')




def load_clients_id_list():
    client_list = []
    try:
        with open(CLIENTS_FILE, 'r') as clients_file:
            clients = clients_file.readlines()
            for client in clients:
                name = client.split(':')[1].strip()
                client_list.append(name)
            clients_file.close
    except FileNotFoundError:
        with open(CLIENTS_FILE, 'w') as clients_file:
            clients_file.close


    except Exception as e:
        print (e)

    return client_list





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