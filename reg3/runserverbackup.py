#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Author: Ariel Yuan, Grace Best
#-----------------------------------------------------------------------

import sys
import argparse
import textwrap
import json
import socket
import http.cookies

#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite'

# Write course information to output
# With specific formatting
def write_courses(courses):
    if courses[0] is False:
        print(f'{sys.argv[0]}: {courses[1]}', file=sys.stderr)
        sys.exit(1)
    # Print output in specified table format
    print('ClsId', 'Dept', 'CrsNum', 'Area', 'Title')
    print('-----', '----', '------', '----', '-----')
    space_num = 5+1+4+1+6+1+4+1
    for row in courses[1]:
        for line in textwrap.wrap('%5s %4s %6s %4s %s'
                                    % (row['classid'], row['dept'],
                                        row['coursenum'], row['area'],
                                        row['title']),
                                    width = 72,
                                    subsequent_indent =
                                    ' ' * space_num):
            print(line)

#-----------------------------------------------------------------------

# Main function to accept command-line
# Arguments and send to the server
# As well as accept database information
# From the server to be printed to output
def main():

    # Ensure correct number of inputs
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} port", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Use argparse to parse arguments
        # and classify them into different options
        des = 'The registrar application: '
        port_help = ''.join(('the port at which the ',
                                'server should listen'))
        ap = argparse.ArgumentParser(description = des)
        ap.add_argument('port', type = int,
                        help = port_help)
        ns = ap.parse_args()
        dict = {'dept':'', 'coursenum':'',
                'area':'', 'title':''}
        args = ('get_overviews', dict)
        with socket.socket() as sock:
            sock.connect((ns.host, ns.port))
            with sock.makefile(mode='w', encoding='utf-8') as flo:
                flo.write(json.dumps(args) + '\n')
                flo.flush()
            with sock.makefile(mode='r', encoding='utf-8') as flo:
                json_str = flo.readline()

            json_str = json_str.rstrip()

            write_courses(json.loads(json_str))


    # Write the Exception message contained within
    # the thrown Exception object to stderr
    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
