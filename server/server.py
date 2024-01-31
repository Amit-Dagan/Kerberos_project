import socket
import os
import logging
import uuid
from hashlib import sha256
import datetime
import json

logging.basicConfig(level=logging.INFO)
CLIENTS_FILE = "clients.txt"
DEFAULT_PORT = 1256

def read_port_from_file():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'port.info')
        with open(file_path, 'r') as port_file:
            return int(port_file.read())
    except Exception as e:
        logging.warning(f"port.info not found or invalid. Using default port {DEFAULT_PORT}. Error: {e}")
        return DEFAULT_PORT

def load_message_server_details():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'msg.info')
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) < 4: raise ValueError("Invalid msg.info format")
            ip_address, port = lines[0].strip().split(':')
            return {
                'ip_address': ip_address,
                'port': int(port),
                'server_name': lines[1].strip(),
                'unique_identifier': lines[2].strip(),
                'symmetric_key_base64': lines[3].strip()
            }
    except Exception as e:
        logging.error(f"Failed to load msg.info: {e}")
        return None

def check_and_register_client(request_json):
    client_name, client_password = request_json.get("Payload", {}).get("Name"), request_json.get("Payload", {}).get("Password")
    if not all([client_name, client_password]):
        return {
            'Header': {
                'Code': 1601
            },
            'Payload': {
                'Message': 'Invalid client data'
            }
        }

    clients = load_clients()
    if client_name in clients:
        return {
            'Header': {
                'Code': 1601
            },
            'Payload': {
                'Message': 'Client name exists'
            }
        }

    new_client_id = str(uuid.uuid4())
    password_hash = sha256(client_password.encode()).hexdigest()
    clients[client_name] = {
        "ID": new_client_id,
        "Name": client_name,
        "PasswordHash": password_hash,
        "LastSeen": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(CLIENTS_FILE, 'a') as file:
            file.write(f"{new_client_id}:{client_name}:{password_hash}:{clients[client_name]['LastSeen']}\n")
    except Exception as e:
        logging.error(f"Failed to save client: {e}")
        return {
            'Header': {
                'Code': 1601
            },
            'Payload': {
                'Message': 'Failed to save client'
            }
        }

    return {
        'Header': {
            'Code': 1600
        },
        'Payload': {
            'Message': 'Registration successful',
            'Client ID': new_client_id
        }
    }

def load_clients():
    clients = {}
    try:
        with open(CLIENTS_FILE, 'r') as file:
            for line in file:
                client_id, name, password_hash, last_seen = line.strip().split(":")
                clients[name] = {
                    "ID": client_id,
                    "Name": name,
                    "PasswordHash": password_hash,
                    "LastSeen": last_seen
                }
    except FileNotFoundError:
        logging.warning(f"{CLIENTS_FILE} not found. Starting with an empty client list.")
    except Exception as e:
        logging.error(f"Failed to load clients: {e}")
    return clients

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', read_port_from_file()))
    server_socket.listen(5)
    logging.info(f"Server listening")

    while True:
        client_socket, _ = server_socket.accept()
        try:
            request = json.loads(client_socket.recv(1024).decode("utf-8"))
            response = check_and_register_client(request) if request.get("Header", {}).get("Code") == 1024 else {
                'Header': {
                    'Code': 400
                },
                'Payload': {
                    'Message': 'Invalid request code'
                }
            }
            client_socket.sendall(bytes(json.dumps(response), "utf-8"))
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    main()
