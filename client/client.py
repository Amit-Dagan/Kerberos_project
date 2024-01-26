import socket
import json
import os
import uuid


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

    f = open(file_path, 'r')
    name = f.readline()
    id = f.readline()
    print(f"name = {name}id = {id}")
except Exception as e:
    print(e)

    f = open(file_path, 'w')
    name = input("Enter your full name: ")+'\n'
    
    s.send(bytes(name, "utf-8"))
    msg = s.recv(1024)
    f.write(name)
    print(msg.decode("utf-8"))
    f.write(msg.decode("utf-8"))





s.close()
f.close()







