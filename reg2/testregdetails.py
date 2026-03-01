#!/usr/bin/env python

#-----------------------------------------------------------------------
# testregdetails.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import os
import sys
import argparse

#-----------------------------------------------------------------------

MAX_LINE_LENGTH = 72
UNDERLINE = '-' * MAX_LINE_LENGTH

#-----------------------------------------------------------------------

def parse_args():

    parser = argparse.ArgumentParser(
        description=
        "Test the Registrar's application's handling of " +
        "class details requests")
    parser.add_argument('program', metavar='program', type=str,
        help='the client program to run')
    parser.add_argument('host', metavar='host', type=str,
        help='the host on which the server is running')
    parser.add_argument('port', metavar='port', type=int,
        help='the port at which the server is listening')
    args = parser.parse_args()

    return (args.program, args.host, args.port)

#-----------------------------------------------------------------------

def print_flush(message):
    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------

def exec_command(program, args):

    print_flush(UNDERLINE)
    command = 'python3 ' + program + ' ' + args
    print_flush(command)
    exit_status = os.system(command)
    if os.name == 'nt':  # Running on MS Windows?
        print_flush('Exit status = ' + str(exit_status))
    else:
        print_flush('Exit status = ' + str(os.WEXITSTATUS(exit_status)))

#-----------------------------------------------------------------------

def main():

    program, host, port = parse_args()

    prefix = host + ' ' + str(port) + ' '

    # Test for help page content
    exec_command(program, '-h')


    # Test for classes with multiple
    # professors or departments
    # and long descriptions
    exec_command(program, prefix + '8321')
    exec_command(program, prefix + '9032')
    exec_command(program, prefix + '8293')
    exec_command(program, prefix + '9977')
    exec_command(program, prefix + '9012')
    exec_command(program, prefix + '10188')

    # Test for no positional arguments
    exec_command(program, prefix + '')
    # Test for too many command line args
    exec_command(program, prefix + '8321 9032')
    # Test for non-compatible argument type
    exec_command(program, prefix + 'abc123')
    # Test for non-existent class
    exec_command(program, prefix + '9034')

    #Test for course withot prof:
    exec_command(program, prefix + '8324')

    # Stress Test:
    for i in range(7000, 7200):
        exec_command(program, prefix + str(i))

if __name__ == '__main__':
    main()
