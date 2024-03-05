import os
import subprocess
import time

# Define the folders and corresponding Python file names
folders = ["auth server", "msg server", "client"]

# Function to run Python files in the specified folder
def run_python_file(folder):
    python_file = os.path.join(folder, f"{folder.replace(' ', '_')}.py")
    subprocess.Popen(["python", python_file], creationflags=subprocess.CREATE_NEW_CONSOLE)

# Get the full path to the current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# Run the authentication server
print("Starting authentication server...")
run_python_file(os.path.join(current_directory, folders[0]))
time.sleep(2)  # Give some time for the server to start

# Run the message server
print("Starting message server...")
run_python_file(os.path.join(current_directory, folders[1]))
time.sleep(2)  # Give some time for the server to start

# Run the client
print("Starting client...")
run_python_file(os.path.join(current_directory, folders[2]))
