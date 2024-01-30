import socket
import uuid
import json


def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))
    s.listen(5)

    while True:
        clientsocket, adress = s.accept()
        print(f"Connection from {adress}")    
        msg = clientsocket.recv(1024)
        data = json.loads(msg.decode('utf-8'))
        print(data)
        if data['Header']['Code'] == 1024:
            #
            id = uuid.uuid4()
            id_str = str(id)

            msg_return = {
                'Header': {
                    'Version': 24,
                    'Code': 1600,
                    'Payload Size': 4
                },
                'Payload': {
                    'ClientID': id_str
                }
            }
            clientsocket.send(bytes(json.dumps(data), "utf-8"))

        

        

def sign_up(name):
    #check if the name is in clients
    return uuid.uuid4()

if __name__ == "__main__":
    main()