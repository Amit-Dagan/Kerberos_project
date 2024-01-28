import socket
import json
import os
import uuid
import hashlib

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect(('10.0.0.19', 1234))
    msg = s.recv(1024)
    print(msg.decode("utf-8"))

except Exception as e:
    print(f"An error occurred: {e}")


name = ""
id = ""

current_directory = os.path.dirname(os.path.abspath(__file__))
file_name = 'me.info'
file_path = os.path.join(current_directory, file_name)
    
try:
    1/0
    f = open(file_path, 'r')
    name = f.readline()
    id = f.readline()
    print(f"name = {name}id = {id}")
except Exception as e:
    print(e)

    f = open(file_path, 'w')
    # name = input("Enter your full name: ")
    # password = input("Enter password: ")

    hash = hashlib.sha256()
    hash.update(b"{password}")
    data = {
        'Header': {
            'Client ID': '',
            'Version': 24,
            'Code': 1024,
            'Payload Size': 4
        },
        'Payload': {
            'Name': name,
            'Password': hash.digest
        }
    }

    print(data)
    
    

    # s.send(bytes(json.dumps(data), "utf-8"))
    # msg = s.recv(1024)
    # f.write(name)
    # f.write('\n')
    # print(msg.decode("utf-8"))
    # f.write(msg.decode("utf-8"))





s.close()
f.close()










