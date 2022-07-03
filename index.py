#!/usr/bin/env python3

import csv
import os
import cgi
import cgitb


codes_filename = 'codes.csv'
assign_filename = 'assigned.txt'


codes = []

print('Content-Type: text/html')
print('')

clientip = os.environ.get('REMOTE_ADDR')
client_found = 0
new_code = 'none'

# Open codes file and read all codes
with open(codes_filename, mode='r') as file:
    codesFile = csv.reader(file)
    for codes_in_a_line in codesFile:
        codes = codes + codes_in_a_line
try:
    # Check if file exists
    filestat = os.stat(assign_filename)
except:
    # File doesn't exist
    f = open(assign_filename, 'w')
    filestat = os.stat(assign_filename)
    f.close()

if filestat.st_size > 0:
    with open(assign_filename, 'r') as file:
        lines = file.readlines()
        # Look if client has already a code assigned
        for line in lines:
            if line.find(clientip+":") != -1:
                client_found = 1 
                break
        # Look for next unused code
        for next_code in codes:
            for line in lines:
                if line.find(":"+next_code) == -1:
                    new_code = next_code
                    break
else:
    new_code = codes[1]

print('<html>')
print('<head>')
print('<title>Welcome</title>')
print('</head>')
print('<body>')
print('<h2>Hello Fellow from ' + clientip + '</h2>')

print('<h2>')
print('<br>')
if client_found == 1:
    print('You have a KEY')
else:
    print('You would need a new key<br>\n')
    print('Your code is:' +new_code)
    f = open(assign_filename,'a')
    f.write(clientip+":"+new_code+"\n")
    f.close()


print('</h2>')
print('</body>')
print('</html>')

