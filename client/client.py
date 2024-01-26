import socket
import json


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect(('10.0.0.19', 1234))
    msg = s.recv(1024)
    print(msg.decode("utf-8"))

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    s.close()

