#!/usr/bin/env python

#-----------------------------------------------------------------------
# testregoverviews.py
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
        print('usage: ' + sys.argv[0] + ' regprogram', file=sys.stderr)
        sys.exit(1)

    program = sys.argv[1]

    # Test for displaying all classes
    exec_command(program, '')

    # Tests for optional commands
    # (found on assignment website)
    exec_command(program, '-d COS')
    exec_command(program, '-n 333')
    exec_command(program, '-n b')
    exec_command(program, '-a Qr')
    exec_command(program, '-t intro')
    exec_command(program, '-t science')
    exec_command(program, '-t C_S')
    exec_command(program, '-t c%S')
    exec_command(program, '-d cos -n 3')
    exec_command(program, '-d COS -a qr -n 2 -t intro')
    exec_command(program, '-t "Independent Study"')
    exec_command(program, '-t "Independent Study "')
    exec_command(program, '-t "Independent Study  "')
    exec_command(program, '-t " Independent Study"')
    exec_command(program, '-t "  Independent Study"')
    exec_command(program, '-t=-c')

    # Test for classes with long titles
    exec_command(program, '-t Topics in Policy Analysis (Half-Term): Management of Public Organizations')

    # Error Handling Examples:
    # (from assignment website)
    exec_command(program, 'a qr')
    exec_command(program, '-A qr')
    exec_command(program, '"-a " qr')
    exec_command(program, '-a qr st')
    exec_command(program, '-a')
    exec_command(program, '-a qr -d')
    exec_command(program, '-a -d')
    exec_command(program, '-x')


#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
