import os
import subprocess
import time

# Define the paths to the Python files
auth_server_path = os.path.join("Kerberos_project", "auth server", "server.py")
msg_server_path = os.path.join("msg server", "msg new.py")
client_path = os.path.join("client", "client.py")

# Run the authentication server
print("Starting authentication server...")
try:
    subprocess.Popen(["python", auth_server_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
except Exception as e:
    print(e)
time.sleep(2)  # Give some time for the server to start

# Run the message server
print("Starting message server...")
subprocess.Popen(["python", msg_server_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
time.sleep(2)  # Give some time for the server to start

# Run the client
print("Starting client...")
subprocess.Popen(["python", client_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
