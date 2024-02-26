import binascii
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
            client_id = file.readline()
            print('client id = ', client_id)


    except FileNotFoundError:
        while (not sign_up()): 
            print('try again')
        

    except Exception as e:
        print(f'error: {e}')

    data = request_key()
    print(data)


    #chat with massage server
        




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
    name = input("Enter your full name: ")
    # TODO if name longer then 255 bytes ask again!

    password = input("Enter password: ")
    # TODO if password longer then 255 bytes ask again!

    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    #print(password_hash)

    password_hash_bytes = password_hash.encode('utf-8')
    name_bytes = name.encode('utf-8')  # Convert to bytes
    client_id = get_random_bytes(16)

    payload_size = 255*2

    data = struct.pack(f'16sBHI255s255s', client_id, VERSION, code, payload_size, name_bytes, password_hash_bytes)
    #print(data)

    s.sendall(data)
    s.listen
    server_answer = s.recv(1024)
    s.close

    version, code, payload_size = struct.unpack(HEADER_FORMAT, server_answer[:HEADER_SIZE])
    #print(server_answer)

    if(code == 1600):
        create_file()
        client_id = struct.unpack('16s', server_answer[HEADER_SIZE:])[0]
        print(str(client_id))
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
    print('requesting key')

    s = connect_to_auth_server()
    if(s == None):
        print('did not manage to connect to server')
        return None

    mag_server_id = b'64f3f63985f04beb81a0e43321880182'
    code = 1027
    nonce = get_random_bytes(8)

    data = struct.pack(f'16sBHI16s8s', client_id.encode('utf-8'), VERSION, code, 24, mag_server_id, nonce)
    
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



if __name__ == "__main__":
    main()