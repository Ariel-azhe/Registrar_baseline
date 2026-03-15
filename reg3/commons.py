#!/usr/bin/env python

#-----------------------------------------------------------------------
# common.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

def get_footer():

    html_str = f'''
        <hr>
        Created by <a href="https://www.cs.princeton.edu/~rdondero">
        Bob Dondero</a>
        <hr>
        '''

    return html_str

#-----------------------------------------------------------------------

# For testing:

def _test():

    print()
    print(get_footer())

if __name__ == '__main__':
    _test()
