import socket
# init connection to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('0.0.0.0', 8008))
# json YYYY-MM-DD
str = '{"api_key": "API KEY HERE", "command_id": "000001"}'
client.send(b'{"api_key": "API KEY HERE", "command_id": "000020"}')
from_server = client.recv(4096)
client.close()
print(from_server)