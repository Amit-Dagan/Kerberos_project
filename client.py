import socket
import json

# header = {
#     "client id": 123132,
#     "Code":1025,
#     "Version":24,
#     "paylode size":100
#     }

# paylode = {
#       "name":"amit",
#       "password":"asdasda"
#    }

# data = {
#     "header": header,
#     "paylode": paylode
# }


# print(data)

#---------------------------------

# mydata = data

# code = mydata["header"]["Code"]

# if code == 1024:
#     print





s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect(('10.0.0.19', 1234))
    msg = s.recv(1024)
    print(msg.decode("utf-8"))

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    s.close()

#asdasdasd
    #asdas dasd asd asdasf fsdfa