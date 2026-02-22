#!/usr/bin/env python

#-----------------------------------------------------------------------
# regserverprelim.py
# Author: Ariel Yuan, Grace Best
#-----------------------------------------------------------------------

import sys
import contextlib
import sqlite3
import argparse
import textwrap
import socket
import os

#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite'

# Function to formulate the argument passed as x
# in a way that allows escaping special characters
# within it through SQLite ESCAPE
def escape_x(x):
    x_list = list(x)
    subx = x
    index = subx.find('_')
    # find every occurence of '_' in x and inserts a '/' in front
    while index >= 0:
        x_list.insert(index, '/')
        subx = x[index + 1:]
        index = subx.find('_')

    new_x = ''.join(x_list)
    subx = new_x
    x_list = list(new_x)
    index = subx.find('%')
    # find every occurence of '%' in x and inserts a '/' in front
    while index >= 0:
        x_list.insert(index, '/')
        subx = x[index + 1:]
        index = subx.find('%')

    new_x = ''.join(x_list)
    return new_x

def create_courses():
    book0 = {'title': 'C Programming', 'price': 88.55}
    book1 = {'title': 'The Practice of Programming', 'price': 35.14}
    course0 = {'name': 'COS 217', 'book': book0}
    course1 = {'name': 'COS 333', 'book': book1}
    courses = [course0, course1]
    return courses
#-----------------------------------------------------------------------

def handle_client(sock):
    courses = create_courses()
    with sock.makefile(mode='w', encoding='utf-8') as flo:
        for course in courses:
            flo.write(course['name'] + '\n')
            book = course['book']
            flo.write(book['title'] + '\n')
            flo.write(str(book['price']) + '\n')
        #flo.flush()
    print('Wrote to client')
#-----------------------------------------------------------------------

def main():
    if len(sys.argv) != 2:
        print(f'usage: python {sys.argv[0]} port', file=sys.stderr)
        sys.exit(1)
    try:
        port = int(sys.argv[1])
        server_sock = socket.socket()
        print('Opened server socket')
        if os.name != 'nt':
            server_sock.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(('', port))
        server_sock.listen()
        while True:
            try:
                sock, _ = server_sock.accept()
                with sock:
                    print('Accepted connection')
                    handle_client(sock)
            except Exception as ex:
                print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
