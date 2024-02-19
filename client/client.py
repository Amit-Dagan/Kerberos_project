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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((socket.gethostname(), 1234))

except Exception as e:
    print(f"An error occurred: {e}")


def main():
    try:
        with open(file_path, 'r') as file:
            sign_in()

        
    except FileNotFoundError:
        sign_up()
        
        sign_in()

    except Exception as e:
        print('error')

    request_key()




def create_file():
    print('creating file')
    f = open(file_path, 'w')
    f.close


def sign_in():
    print('sign_in')

def sign_up():
    print('sign_up')

    #create_file()
    
    code = 1024  # Registration code
    name = input("Enter your full name: ") + '\x00'
    # TODO if name longer then 255 bytes ask again!

    password = input("Enter password: ")
    # TODO if password longer then 255 bytes ask again!

    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest() + '\x00'
    #print(password_hash)

    password_hash_bytes = password_hash.encode('utf-8')
    name_bytes = name.encode('utf-8')  # Convert to bytes
    client_id = get_random_bytes(16)

    payload_size = 255*2

    data = struct.pack(f'16sBHI255s255s', client_id, VERSION, code, payload_size, name_bytes, password_hash_bytes)
    print(data)

    s.sendall(data)
    s.listen
    print(s.recv(1024))


    return data



def request_key():
    print('requesting key')



if __name__ == "__main__":
    main()