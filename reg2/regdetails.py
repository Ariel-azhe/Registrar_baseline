#!/usr/bin/env python

#-----------------------------------------------------------------------
# regdetails.py
# Author: Ariel Yuan, Grace Best
#-----------------------------------------------------------------------

import sys
import contextlib
import sqlite3
import textwrap
import argparse
import json
import socket
#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite'

def write_class(class_detail):
    if class_detail[0] == False:
        print(f'{class_detail[1]}', file=sys.stderr)
        sys.exit(1)
    details = class_detail[1]
    print('-------------')
    print('Class Details')
    print('-------------')
    print('Class Id:', details['classid'])
    # Store the class' courseid in a variable
    print('Days:', details['days'])
    print('Start time:', details['starttime'])
    print('End time:', details['endtime'])
    print('Building:', details['bldg'])
    print('Room:', details['roomnum'])
    print('--------------')
    print('Course Details')
    print('--------------')
    space_num = 3
    if details['courseid'] != '':
        print('Course Id: ' + details['courseid'])
    else:
        print('Course Id:')
    for cross in details['deptcoursenums']:
        print('Dept and Number:', cross['dept'], cross['coursenum'])
    if details['area'] != '':
        print('Area: ' + details['area'])
    else:
        print('Area:')
    for line in textwrap.wrap(
        'Title: ' + details['title'],
        width = 72,
        subsequent_indent= ' ' * space_num):
        print(line)
    for line in textwrap.wrap(
        'Description: ' + details['descrip'],
        width = 72,
        subsequent_indent= ' ' * space_num):
        print(line)
    for line in textwrap.wrap(
        'Prerequisites: ' + details['prereqs'],
        width = 72,
        subsequent_indent=' ' * space_num):
        print(line)

    for prof in details['profnames']:
        print('Professor:', prof)

def main():
    try:
        host_help = ''.join(('the computer on which the ',
                                'server is running'))
        port_help = ''.join(('the port at which the ',
                                'server is listening'))
        reg_desc = ''.join(('Registrar application: ',
                            'show details about a class'))
        classid_help = ''.join(('the id of the class whose ',
                                'details should be shown'))
        parser = argparse.ArgumentParser(description = reg_desc)
        # Parse the command line argument as the classid
        parser.add_argument('host', type = str,
                        help = host_help)
        parser.add_argument('port', type = int,
                        help = port_help)
        parser.add_argument('classid', type = int,
                            help = classid_help)
        ns = parser.parse_args()
        args = ('get_details', ns.classid)
        json_str = json.dumps(args)
        with socket.socket() as sock:
            sock.connect((ns.host, ns.port))
            with sock.makefile(mode='w', encoding='utf-8') as flo:
                flo.write(json_str + '\n')
                flo.flush()
            with sock.makefile(mode='r', encoding='utf-8') as flo:
                json_str = flo.readline()
            json_str = json_str.rstrip()
            details = json.loads(json_str)
            write_class(details)
                
    # Write the Exception message contained within
    # the thrown Exception object to stderr
    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
