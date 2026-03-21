#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Author: Ariel Yuan & Grace Best
#-----------------------------------------------------------------------

import sys
import wsgiref.simple_server
import penny

def main():

    if len(sys.argv) != 2:
        print(f'usage: {sys.argv[0]} port', file=sys.stderr)
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except Exception:
        print(f'{sys.argv[0]}: Port must be an integer.',
              file=sys.stderr)
        sys.exit(1)

    try:
        penny.app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
