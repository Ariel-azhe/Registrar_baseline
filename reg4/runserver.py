#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Author: Ariel Yuan & Grace Best
#-----------------------------------------------------------------------

import sys
import argparse
import registrar

def main():

    try:
        # description to be displayed on -h page
        port_help = ''.join(('the port at which the ',
                                'should listen'))
        reg_desc = ''.join(('The registrar application'))
        parser = argparse.ArgumentParser(description = reg_desc)
        # Parse the command line argument as the port
        parser.add_argument('port', type = int,
                        help = port_help)
        ns = parser.parse_args()
    # Write the Exception message contained within
    # the thrown Exception object to stderr
    except Exception:
        print(f'{sys.argv[0]}: Port must be an integer.',
              file=sys.stderr)
        sys.exit(1)

    try:
        registrar.app.run(host='0.0.0.0', port=ns.port, debug=True)

    # Write the Exception message contained within
    # the thrown Exception object to stderr
    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
