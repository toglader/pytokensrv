#!/usr/bin/env python3

import csv
import os
import ipaddress
import sys
import cgi
import cgitb


# Location of files
tokens_filename = 'tokens.csv'
assign_filename = 'assigned.txt'
deny_filename = 'denyhosts.txt'



    

def main():
    # Initialize variables
    tokens = []
    clientip = os.environ.get('REMOTE_ADDR')
    client_found = 0
    new_token = ''

    print('Content-Type: text/html')
    print('')

    # Check if user is allowed to user service
    if not check_if_allowed(clientip):
        print_page_header()
        print('Go away!')
        print_page_footer()
        exit()

    # Read tokens from file
    tokens_file = open(tokens_filename, mode='r')
    tokens = csv.DictReader(tokens_file)

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
            
            # Look if client has already a token assigned
            for line in lines:
                if line.find(clientip+":") != -1:
                    client_found = 1 
                    break
            
            # Look for next unused code
            for token_row in tokens:
                for line in lines:
                    # Check if token is assigned already
                    if line.find(":"+token_row['token']) == -1:
                        # token unused
                        new_token = token_row
                        break
            
            file.close()
    else:
        # Assigned filesize is zero. Use first token
        for token_row in tokens:
            new_token = token_row
            break


    print_page_header()
    print('<h2>Hello Fellow from ' + clientip + '</h2>')

    print('<h2>')
    print('<br>')

    if client_found == 1:
        print('You have a token already')
    else:
        if new_token == '':
            print('Sorry! Out of tokens. Please come back again later.')
        else:
            print('You would need a new token<br>\n')
            print('Your token is: ' +new_token['formatted token'] + '<br>\n')
            print('Expiration date: ' + new_token['expiry date'] + '<br>\n')
            f = open(assign_filename,'a')
            f.write(clientip + ':' + new_token['token']+'\n')
            f.close()
            print('NOTE! Keep your token safe, you are not able to retrieve it again from this service!')


    print('</h2>')
    print_page_footer()

    # Close files
    tokens_file.close()

def check_if_allowed(ip):
    allowed = True

    try:
        # Check if file exists
        filestat = os.stat(deny_filename)

        if filestat.st_size > 0:
            with open(deny_filename, 'r') as file:
                lines = file.readlines()
                # Loop trhough lines and skip comments and empty lines
                for line in lines:
                    network = line.strip().replace('\n', '').replace('\r', '')
                    if not network.startswith('#') and len(network) > 0:
                        if ipaddress.ip_address(ip) in ipaddress.ip_network(network):
                            allowed = False
                            file.close()
                            break
    
    except:
        # File does not exist, or read failed
        sys.stderr.write('Unable to open file ' + deny_filename)
        allowed = False
    return allowed

def print_page_header():
    print('<html>')
    print('<head>')
    print('<title>Welcome</title>')
    print('</head>')
    print('<body>')

def print_page_footer():
    print('</body>')
    print('</html>')


if __name__ == "__main__":
    main()


