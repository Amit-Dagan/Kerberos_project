import socket
import uuid

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('10.0.0.19', 1234))
s.listen(5)

while True:
    clientsocket, adress = s.accept()
    print(f"Connection from {adress}")    
    clientsocket.send(bytes("Welcom", "utf-8"))
    msg = clientsocket.recv(1024)
    id = uuid.uuid4()
    id_str = str(id)
    print(id)
    clientsocket.send(bytes(id_str, "utf-8"))

#change  
ptint("asdasd")