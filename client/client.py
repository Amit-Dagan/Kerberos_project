import binascii
import datetime
import socket
import struct
import hashlib
import os
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

current_directory = os.path.dirname(os.path.abspath(__file__))
file_name = 'me.info'
file_path = os.path.join(current_directory, file_name)

VERSION = 24
HEADER_FORMAT = 'BHI'
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
client_id = ''

def main():
    try:
        with open(file_path, 'r') as file:
            name = file.readline()
            global client_id
            client_id_hex = file.readline()
            client_id = binascii.unhexlify(client_id_hex)
    

    except FileNotFoundError:
        while (not sign_up()): 
            print('try again')
        

    except Exception as e:
        print(f'error: {e}')


    data = request_key()
    print(data)

    s = connect_to_msg_server()
    send_key(s, data)
    chat(s, data)

    #chat with massage server
        

def send_key(s, data):
    global client_id
    authenticator = create_authenticator(data['key'])


    payload_format = f'{len(authenticator)}s{len(data['ticket'])}s'
    payload = struct.pack(payload_format, authenticator, data['ticket'])
    
    headers = struct.pack('16sBHI', client_id, VERSION, 1028, struct.calcsize(payload_format))

    msg = struct.pack(f'{struct.calcsize('16sBHI')}s{struct.calcsize(payload_format)}s', headers, payload)
    
    s.sendall(msg)


def create_authenticator(key):
    global client_id
    auth_headers = '16s16s16s16s8s'
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode()
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_version = cipher.encrypt(pad(str(VERSION).encode('utf-8'), AES.block_size))
    encrypted_client_id = cipher.encrypt(client_id)
    encrypted_server_id = cipher.encrypt(client_id)
    encrypted_creation_time = cipher.encrypt(pad(current_time, AES.block_size))
    iv = cipher.iv
    authenticator = struct.pack(auth_headers, iv, encrypted_version, encrypted_client_id, encrypted_server_id, encrypted_creation_time)
    
    return authenticator

def connect_to_msg_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect(('127.0.0.1', 1235))
        return s

    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None

    print("connect_to_msg_server")

def chat(s, dict_data):
    global client_id
    print(dict_data['ticket'])
    s.sendall(dict_data['ticket'])
    print("chat")

def connect_to_auth_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((socket.gethostname(), 1234))
        return s

    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None

def create_file():
    print('creating file')
    f = open(file_path, 'w')
    f.close

def sign_up():
    print('sign_up')
    
    s = connect_to_auth_server()
    
    if(s == None):
        print('did now manage to connect to server')
        return None

    code = 1024  # Registration code

    name = valid_input('Enter a name')
    password = valid_input("Enter password: ")

    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    password_hash_bytes = password_hash.encode('utf-8')
    name_bytes = name.encode('utf-8')  # Convert to bytes
    rand_client_id = get_random_bytes(16)

    payload_size = 255*2

    data = struct.pack(f'16sBHI255s255s', rand_client_id, VERSION, code, payload_size, name_bytes, password_hash_bytes)

    s.sendall(data)
    s.listen
    server_answer = s.recv(1024)
    s.close

    version, code, payload_size = struct.unpack(HEADER_FORMAT, server_answer[:HEADER_SIZE])

    if(code == 1600):
        create_file()
        global client_id
        client_id = struct.unpack('16s', server_answer[HEADER_SIZE:])[0]
        client_id_hex = binascii.hexlify(client_id).decode()
        print('success')

        try:
            with open(file_path, 'w') as client_info:
                client_info.write(name)
                client_info.write('\n')
                client_info.write(client_id_hex)
                print('asd')
                client_info.close
                return True
            
        except Exception as e:
            print(e)
    else:
        print('fail')
    
    return False

def request_key():
    global client_id
    print('requesting key')
    print('client id = ', client_id)

    s = connect_to_auth_server()
    if(s == None):
        print('did not manage to connect to server')
        return None

    mag_server_id = b'64f3f63985f04beb81a0e43321880182'
    code = 1027
    nonce = get_random_bytes(8)

    data = struct.pack(f'16sBHI16s8s', client_id, VERSION, code, 24, mag_server_id, nonce)
    
    s.sendall(data)
    s.listen
    server_answer = s.recv(1024)
    s.close

    encrypted_key_headers = '16s16s32s'
    ticket_headers = 'B16s16s8s16s32s8s'
    data_headers = f'16s{struct.calcsize(encrypted_key_headers)}s{struct.calcsize(ticket_headers)}s'
    client_id_returned , encrypted_key, ticket = struct.unpack(data_headers, server_answer)

    iv, encrypted_nonce, encrypted_aes_key = struct.unpack(encrypted_key_headers, encrypted_key)
    
    while(True):
        password = input("Enter password: ")
        password_hash = hashlib.sha256(password.encode('utf-8')).digest()

        cipher = AES.new(password_hash, AES.MODE_CBC, iv)
        decrypted_nonce = cipher.decrypt(encrypted_nonce)
        try:
            decrypted_nonce = unpad(decrypted_nonce, AES.block_size)
        except ValueError as ve:
            continue
        except Exception as e:
            print(e)

        if(nonce == decrypted_nonce):
            break
    
    decrypted_aes_key = cipher.decrypt(encrypted_aes_key)
    try:
        decrypted_aes_key = unpad(decrypted_aes_key, AES.block_size)
    except Exception as e:
        print(e)
    return {'ticket': ticket, 'key': decrypted_aes_key}

def valid_input(str):
    
    user_input = input(str).strip()
    while (len(user_input) > 255):
        user_input = input("please enter less then 255 characters").strip()
    return user_input





if __name__ == "__main__":
    main()