import binascii
import random
import socket
import struct
import sys
import uuid
import hashlib
import os
from Crypto.Random import get_random_bytes

current_directory = os.path.dirname(os.path.abspath(__file__))
file_name = 'me.info'
file_path = os.path.join(current_directory, file_name)

VERSION = 24
HEADER_FORMAT = 'BHI'
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((socket.gethostname(), 1234))

except Exception as e:
    print(f"An error occurred: {e}")


def main():
    try:
        with open(file_path, 'r') as file:
            request_key()

        
    except FileNotFoundError:
        create_file()
        sign_up() 
        request_key()
  

    except Exception as e:
        print(f'error: {e}')

    #chat with massage server
        




def create_file():
    print('creating file')
    f = open(file_path, 'w')
    f.close


def sign_in():
    print('sign_in')

def sign_up():
    print('sign_up')
    
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

    version, code, payload_size = struct.unpack(HEADER_FORMAT, server_answer[:HEADER_SIZE])
    #print(server_answer)

    if(code == 1600):
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
        except Exception as e:
            print(e)
    else:
        print('fail')

    return data



def request_key():
    client_id = b'64f3f63985f04beb81a0e43321880182'
    mag_server_id = b'64f3f63985f04beb81a0e43321880182'
    code = 1027
    nounce = get_random_bytes(8)
    data = struct.pack(f'16sBHI16s8s', client_id, VERSION, code, 24, mag_server_id, nounce)
    s.sendall(data)

    
    print('requesting key')



if __name__ == "__main__":
    main()