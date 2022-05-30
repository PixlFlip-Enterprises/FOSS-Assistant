import socket

# input for connecting to server
# profileInput = input("Enter Your User Profile: ")
# profilePassword = input("Enter Your Password: ")
# Now infinite loop with basic commands from FOSS Assistant Main instance
end = False
while not end:

    # init connection to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('0.0.0.0', 8008))
    # json YYYY-MM-DD
    str = '{"api_key": "API KEY HERE", "command_id": "000001"}'
    client.send(b'{"api_key": "API KEY HERE", "command_id": "000020"}')
    from_server = client.recv(4096)
    client.close()
    print(from_server)
    end = True


# TODO DONT YOU DARE POST THIS UNTIL YOU MAKE SURE IT HAS NO COMPROMISING DATA IN IT!!!