"""
comtact_importer.py Version 1
Author: PixlFlip
Date: June 25, 2022

Needed a script to import my Apple contacts
so decided I might as well at it to the client examples.
"""
import socket
import csv
import time

# csv file name
filename = "Contacts.csv"

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
for contact in rows:
    # compile data
    if contact[31] == '':
        json_to_send = '{"api_key": "YOUR API KEY HERE", "command_id": "000030", "f_name": "' + contact[
            0] + '", "l_name": "' + contact[1] + '", "display_name": "' + contact[2] + '", "nickname": "' + contact[
                           3] + '", "email_address": "' + contact[4] + '", "email_address2": "' + contact[
                           5] + '", "email_address3": "' + contact[6] + '", "home_phone": "' + contact[
                           7] + '", "business_phone": "' + contact[8] + '", "home_fax": "' + contact[
                           9] + '", "business_fax": "' + contact[10] + '", "pager": "' + contact[
                           11] + '", "mobile_phone": "' + contact[12] + '", "home_address": "' + contact[
                           13] + '", "home_address2": "' + contact[14] + '", "home_city": "' + contact[
                           15] + '", "home_state": "' + contact[16] + '", "home_postal_code": "' + contact[
                           17] + '", "home_street": "' + contact[18] + '", "business_address": "' + contact[
                           19] + '", "business_address2": "' + contact[20] + '", "business_city": "' + contact[
                           21] + '", "business_state": "' + contact[22] + '", "business_postal": "' + contact[
                           23] + '", "business_country": "' + contact[24] + '", "country_code": "' + contact[
                           25] + '", "related_names": "' + contact[26] + '", "job": "' + contact[
                           27] + '", "department": "' + contact[28] + '", "organization": "' + contact[
                           29] + '", "notes": "' + contact[
                           30] + '", "birthday": "2000/01/01", "anniversary": "2000/01/01", "gender": "' + contact[
                           33] + '", "website": "' + contact[34] + '", "website2": "' + contact[
                           35] + '", "categories": "' + contact[
                           36] + '", "sociological_options": "NONE", "social_media": "NONE", "discord": "NONE", "personality_rating": "-1", "trust_score": "-1", "known_since": "NONE"}'
    else:
        json_to_send = '{"api_key": "YOUR API KEY HERE", "command_id": "000030", "f_name": "' + contact[0] + '", "l_name": "' + contact[1] + '", "display_name": "' + contact[2] + '", "nickname": "' + contact[3] + '", "email_address": "' + contact[4] + '", "email_address2": "' + contact[5] + '", "email_address3": "' + contact[6] + '", "home_phone": "' + contact[7] + '", "business_phone": "' + contact[8] + '", "home_fax": "' + contact[9] + '", "business_fax": "' + contact[10] + '", "pager": "' + contact[11] + '", "mobile_phone": "' + contact[12] + '", "home_address": "' + contact[13] + '", "home_address2": "' + contact[14] + '", "home_city": "' + contact[15] + '", "home_state": "' + contact[16] + '", "home_postal_code": "' + contact[17] + '", "home_street": "' + contact[18] + '", "business_address": "' + contact[19] + '", "business_address2": "' + contact[20] + '", "business_city": "' + contact[21] + '", "business_state": "' + contact[22] + '", "business_postal": "' + contact[23] + '", "business_country": "' + contact[24] + '", "country_code": "' + contact[25] + '", "related_names": "' + contact[26] + '", "job": "' + contact[27] + '", "department": "' + contact[28] + '", "organization": "' + contact[29] + '", "notes": "' + contact[30] + '", "birthday": "' + contact[31] + '", "anniversary": "2000/01/01", "gender": "' + contact[33] + '", "website": "' + contact[34] + '", "website2": "' + contact[35] + '", "categories": "' + contact[36] + '", "sociological_options": "NONE", "social_media": "NONE", "discord": "NONE", "personality_rating": "-1", "trust_score": "-1", "known_since": "NONE"}'

    # init server stuff
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server
    client.connect(('0.0.0.0', 8008))
    print('Contact ' + contact[0] + ' has been imported.')
    sending_data = bytes(json_to_send, 'utf-8')
    client.send(sending_data)
    from_server = client.recv(4096)
    client.close()
    print(from_server)
    time.sleep(2)