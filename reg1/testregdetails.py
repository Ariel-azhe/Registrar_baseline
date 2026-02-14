#!/usr/bin/env python

#-----------------------------------------------------------------------
# testregdetails.py
# Author: Ariel Yuan, Grace Best
#-----------------------------------------------------------------------

import os
import sys

#-----------------------------------------------------------------------

MAX_LINE_LENGTH = 72
UNDERLINE = '-' * MAX_LINE_LENGTH

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

    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' regdetailsprogram',
            file=sys.stderr)
        sys.exit(1)

    program = sys.argv[1]

    # Test for help page content
    exec_command(program, '-h')


    # Test for classes with multiple
    # professors or departments
    # and long descriptions
    exec_command(program, '8321')
    exec_command(program, '9032')
    exec_command(program, '8293')
    exec_command(program, '9977')
    exec_command(program, '9012')
    exec_command(program, '10188')

    # Test for no positional arguments
    exec_command(program, '')
    # Test for too many command line args
    exec_command(program, '8321 9032')
    # Test for non-compatible argument type
    exec_command(program, 'abc123')
    # Test for non-existent class
    exec_command(program, '9034')

    #Test for course withot prof:
    exec_command(program, '8324')

    # Stress Test:
    for i in range(7000, 7200):
        exec_command(program, str(i))

if __name__ == '__main__':
    main()
