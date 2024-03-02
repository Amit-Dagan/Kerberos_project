import binascii
from Crypto.Random import get_random_bytes


client_id = get_random_bytes(16)

client_id_hex = binascii.hexlify(client_id).decode()

original_id = binascii.unhexlify(client_id_hex)

print(client_id)
print(client_id_hex)
print(original_id)