import socket
import uuid
import json
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
clients_path = os.path.join(current_directory, 'clients')

port = 1256
clients_dict = {}

def main():

    file_name = 'port.info'
    file_path = os.path.join(current_directory, file_name)
        
    try:
        #1/0
        f = open(file_path, 'r')
        port_str = f.readline()
        port = int(port_str)


    except Exception as e:
        print("using defult port")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), port))
    s.listen(5)

    while True:
        clientsocket, adress = s.accept()
        print(f"Connection from {adress}")    
        msg = clientsocket.recv(1024)
        data = json.loads(msg.decode('utf-8'))
        print(data)
        if data['Header']['Code'] == 1024:
            #
            if data['Payload']['Name'] in clients_dict:
                print("taken")

            else:
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
                clients_dict[data['Payload']['Name']] = {
                    'ID': id_str,
                    'PasswordHash': data['Payload']['Password'],
                    'LastSeen': 1
                }
                with open(clients_path, 'w+') as clients_file:
                    user_str = f"{id_str}:{data['Payload']['Name']}:{data['Payload']['Password']}:{1}\n"
                    clients_file.write(user_str)


        

        

def sign_up(name):
    #check if the name is in clients
    return uuid.uuid4()

def init():
    
    port_name = 'port.info'
    port_path = os.path.join(current_directory, port_name)
        
    try:
        #1/0
        port_file = open(port_path, 'r')
        port = port_file.readline()
        port_file.close

    except Exception as e:
        print("using defult port")

        
    try:
        #1/0
        clients_file = open(clients_path, 'r')
        for line in clients_file:
            
            fields = line.strip().split(':')
            user_id, name, password_hash, last_seen = fields
            user_info = {
                'ID': user_id,
                'PasswordHash': password_hash,
                'LastSeen': last_seen
            }

            clients_dict[name] = user_info
        

    except Exception as e:
        print("creating clients file")
        clients_file = open(clients_path, 'w')
        clients_file.close



if __name__ == "__main__":
    init()
    main()