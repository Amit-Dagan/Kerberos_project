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

current_directory = os.path.dirname(os.path.abspath(__file__))

AUTH_SERVER_IP = '127.0.0.1'
AUTH_SERVER_PORT = 1234
IP = '127.0.0.1'
PORT = 1235
NAME = ''
VERSION = 24
SERVER_ID = 0
AES_KEY = 0

def main():
    print('main')

    srv_file_lines = read_srv_file() 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((IP, PORT))
        
        if (len(srv_file_lines) == 3):
            sign_up(server_socket)
            # while(not sign_up()):
            #     print('please try signing up again')
        else:
            load_server_details(srv_file_lines);
        
        server_socket.listen()
        while True:

            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            client_data = client_socket.recv(1024) 
            header_format = '16sBHI'
            header_size = struct.calcsize(header_format)
            client_id, version, code, payload_size = struct.unpack(header_format, client_data[:header_size])
            print('handeling id: ', client_id)
            if(version != VERSION):
                #TODO check if works
                continue

            if(len(client_data[header_size:]) != payload_size):
                print(f"len of client_data[HEADER_SIZE:] = {len(client_data[header_size:])} ")
                print(f"len of payload_size = {payload_size}")
                print('not the same size')
                #TODO check if works
                continue


            match code:
                case 1028:
                    print('1028')
                    #get_aes_key()
                case 1029:
                    print('1029')
                    #get_message
    




def sign_up():
    print('sign_up')
    s = connect_to_auth_server()
    
    if(s == None):
        print('did now manage to connect to server')
        return None

    code = 1025  # MSG Server registration code
    aes_key = get_random_bytes(32)
    name_bytes = NAME.encode('utf-8')  # Convert to bytes
    rand_msg_id = get_random_bytes(16)
    payload_size = 255+32

    data = struct.pack(f'16sBHI255s32s', rand_msg_id, VERSION, code, payload_size, name_bytes, aes_key)

    s.sendall(data)
    s.listen
    server_answer = s.recv(1024)
    s.close()
    header_format = 'BHI'
    header_size = struct.calcsize(header_format)
    version, code, payload_size = struct.unpack(header_format, server_answer[:header_size])

    if(code == 1600):
        global SERVER_ID
        global AES_KEY
        AES_KEY = aes_key
        SERVER_ID = struct.unpack('16s', server_answer[HEADER_SIZE:])[0]
        server_id_hex = binascii.hexlify(SERVER_ID).decode()
        print('success')
        file_path = os.path.join(current_directory, 'msg.info')

        try:
            with open(file_path, 'a') as msg_info:
                msg_info.write(f'\n{server_id_hex}\n')
                msg_info.write(b64encode(aes_key).decode())
                msg_info.close()
                return True
            
        except Exception as e:
            print(e)
    else:
        print('fail')
    
    return False

def read_srv_file():
    global AUTH_SERVER_IP, AUTH_SERVER_PORT, NAME, IP, PORT

    msg_path = os.path.join(current_directory, 'msg.info')
    
    try:
        with open(msg_path, 'r') as file:
            lines = file.readlines()
            print(lines)
            AUTH_SERVER_IP, AUTH_SERVER_PORT = lines[0].strip().split(':')
            IP, PORT = lines[1].strip().split(':')

            # Convert port numbers to integers
            AUTH_SERVER_PORT = int(AUTH_SERVER_PORT)
            PORT = int(PORT)
            NAME = lines[2].strip()
        return lines
    except FileNotFoundError:
        print('File srv.info not found. Using default values.')

    except Exception as e:
        print(f'Error: {e}')

def connect_to_auth_server(s): 

    try:
        s.connect((AUTH_SERVER_IP, AUTH_SERVER_PORT))
        return s

    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None

def load_server_details(list):
    global SERVER_ID
    global AES_KEY
    SERVER_ID = list[3]
    AES_KEY = list[4]

def valid_input(str):
    
    user_input = input(str).strip()
    while (len(user_input) > 255):
        user_input = input("please enter less then 255 characters").strip()
    return user_input




    

if __name__ == "__main__":
    main()