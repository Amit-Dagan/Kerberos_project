import socket
import os
import logging



#MyChanges


def load_message_server_details():
    try:
        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_name = 'msg.info'
        file_path = os.path.join(current_directory, file_name)

        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Ensure that there are at least 4 lines in the file
            if len(lines) < 4:
                raise ValueError("Invalid msg.info file format")

            # Extract the details from each line
            ip_address, port = lines[0].strip().split(':')
            server_name = lines[1].strip()
            unique_identifier = lines[2].strip()
            symmetric_key_base64 = lines[3].strip()

            # Create a dictionary to store the details
            message_server_details = {
                'ip_address': ip_address,
                'port': int(port),
                'server_name': server_name,
                'unique_identifier': unique_identifier,
                'symmetric_key_base64': symmetric_key_base64
            }

            return message_server_details

    except FileNotFoundError:
        logging.error("msg.info file not found.")
        return None
    except Exception as e:
        logging.error(f"Error reading msg.info: {e}")
        return None




def save_clients():
    try:
        with open('clients', 'w') as clients_file:
            for client_id, data in clients.items():
                clients_file.write(f"{client_id}:{data['name']}:{data['password_hash']}:{data['last_seen']}\n")
        logging.info("Saved client data to file.")
    except Exception as e:
        logging.error(f"Error saving clients to file: {e}")

    # Additionally, update the in-memory data
    # This ensures that the in-memory data is synchronized with the file
    clients_in_memory = clients.copy()
    clients.clear()
    for client_id, data in clients_in_memory.items():
        clients[client_id] = data





#End#MyChanges
    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('10.0.0.19', 1234))
s.listen(5)

while True:
    clientsocket, adress = s.accept()
    print(f"Connection from {adress}")
    clientsocket.send(bytes("Welcom", "utf-8"))




#change




  



    