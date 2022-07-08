"""
journal_importer.py Version 1
Author: PixlFlip
Date: June 26, 2022

Just a quick journal import script
"""
import socket
import csv
import time

# csv file name
filename = "Journal.csv"

# initializing the titles and rows list
fields = []
rows = []

# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)

    # get total number of rows
    print("Total no. of rows: %d" % (csvreader.line_num))

# printing the field names
print('Field names are:' + ', '.join(field for field in fields))

# iterate through contact's info
for journal_entry in rows:
    # compile data
    json_to_send = '{"api_key": "#2AJKLFHW9203NJFC", "command_id": "000021", "date": "' + journal_entry[0] + '", "entry": "' + journal_entry[1] + '", "creation_device": "' + journal_entry[2] + '", "starred": "' + journal_entry[3] + '", "timezone": "' + journal_entry[4] + '"}'
    # init server stuff
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server
    client.connect(('0.0.0.0', 8008))
    print('Contact ' + journal_entry[0] + ' has been imported.')
    sending_data = bytes(json_to_send, 'utf-8')
    client.send(sending_data)
    from_server = client.recv(4096)
    client.close()
    print(from_server)
    time.sleep(2)