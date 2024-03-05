import binascii
from Crypto.Random import get_random_bytes
from base64 import b64encode


# client_id = get_random_bytes(32)
# client_id_hex = binascii.hexlify(client_id).decode()
# original_id = binascii.unhexlify(client_id_hex)
# client_id_b64 = b64encode(client_id).decode()

# id = b'PV8I\x90\x11\xe3\x8et\xbfG\x0c\x90\x8e\x82`'
# print(client_id_b64)


size = (277*5)+5

num = size//277

print(num)