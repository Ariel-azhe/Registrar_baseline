#!/usr/bin/env python

#-----------------------------------------------------------------------
# common.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

def get_header():

    html_str = f'''
        <h1>Registrar's Office</h1>
        '''

    return html_str

#-----------------------------------------------------------------------

def get_footer():

    html_str = f'''
        <hr>
        Created by <a href="https://www.cs.princeton.edu/~rdondero">
        Ariel & Grace</a>
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
