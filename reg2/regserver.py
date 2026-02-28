#!/usr/bin/env python

#-----------------------------------------------------------------------
# regserverprelim.py
# Author: Ariel Yuan, Grace Best
#-----------------------------------------------------------------------

import sys
import contextlib
import sqlite3
import socket
import os
import json
import threading
import time
#-----------------------------------------------------------------------
DATABASE_URL = 'file:reg.sqlite'
CDELAY = int(os.environ.get('CDELAY', '0'))
IODELAY = int(os.environ.get('IODELAY', '0'))

def consume_cpu_time(delay):
    initial_thread_time = time.thread_time()
    while (time.thread_time() - initial_thread_time) < delay:
        pass


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

class CourseThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self._sock = sock

    def run(self):
        print('Spawned child thread')
        # Simulate a compute-bound server.

        with self._sock.makefile(mode='r', encoding='utf-8') as in_flo:
            json_str = in_flo.readline()
            json_str = json_str.rstrip()

        start_time = time.perf_counter()

        args = json.loads(json_str)
        print('received request:', args)
        
        try:
            to_client = search_courses(args)
            json_str = json.dumps(to_client)
            with self._sock.makefile(mode='w', encoding='ascii') as out_flo:
                out_flo.write(json_str + '\n')
                out_flo.flush()
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time:.6f} seconds")
        except Exception as ex:
            to_client = [False, 'A server error occurred. Please contact the system administrator.']
            json_str = json.dumps(to_client)
            with self._sock.makefile(mode='w', encoding='utf-8') as flo:
                flo.write(json_str + '\n')
                flo.flush()
            print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        print('Closed socket in',  args[0], 'thread')
        print('Exiting',  args[0], 'thread')

def search_courses(args):
    time.sleep(IODELAY)
    consume_cpu_time(CDELAY)
    success = True
    with sqlite3.connect(DATABASE_URL + '?mode=ro',
            isolation_level=None, uri=True) as connection:

        with contextlib.closing(connection.cursor()) as cursor:
            if args[0] == 'get_overviews':
                dict = args[1]
                # Select the columns that should be
                # displayed with corresponding courseids
                prepare = []
                stmt_str = '''
                    SELECT classes.classid, crosslistings.dept, 
                    crosslistings.coursenum, courses.area, courses.title
                    FROM classes, crosslistings, courses
                    WHERE 
                    courses.courseid = classes.courseid and courses.courseid = crosslistings.courseid
                    '''
                if dict['dept'] != '':
                    stmt_str += ' AND crosslistings.dept LIKE ? '
                    prepare.append(f'%{dict['dept'].upper()}%')
                if dict['coursenum'] != '':
                    stmt_str += ' AND coursenum LIKE ? '
                    prepare.append(f'%{dict['coursenum']}%')
                if dict['area'] != '':
                    stmt_str += ' AND area LIKE ? '
                    prepare.append(f'%{dict['area'].upper()}%')
                if dict['title'] != '':
                    stmt_str += ' AND title LIKE ? '
                    prepare.append(f'%{escape_x(dict['title'])}%')

                stmt_str += 'ORDER BY dept, coursenum, classid'
                cursor.execute(stmt_str, prepare)
                tab = cursor.fetchall()
                table = []
                for cls in tab:
                    dict = {'classid': cls[0], 'dept': cls[1], 'coursenum':cls[2], 'area': cls[3], 'title': cls[4]}
                    table.append(dict)
#Branch for details
            elif args[0] == 'get_details':
                classid = args[1]
                # Select the columns that should be
                # displayed with corresponding courseids
                table = {'classid':'', 'days':'',
                        'starttime':'',
                        'endtime':'',
                        'bldg':'', 'roomnum':'',
                        'courseid':'',
                        'deptcoursenums':[], 'area':'',
                        'title':'', 'descrip':'',
                        'prereqs':'','profnames': []}
                prepare = []
                cursor.execute(f'''SELECT * FROM classes
                               WHERE classid = ?
                               ''', [classid])
                tab = cursor.fetchall()
                if len(tab) == 0:
                    success = False
                    table = f'{sys.argv[0]}: no class with classid {classid} exists'
                else:
                    for row in tab:
                        table['classid'] = row[0]
                        courseid = row[1]
                        table['days'] = row[2]
                        table['starttime'] = row[3]
                        table['endtime'] = row[4]
                        table['bldg'] = row[5]
                        table['roomnum'] = row[6]
                    cursor.execute(''' SELECT DISTINCT dept, coursenum
                                FROM classes, crosslistings
                                WHERE
                                classes.courseid = crosslistings.courseid
                                AND classes.courseid = ?
                                ORDER BY dept, coursenum
                                ''', [courseid])
                    tab = cursor.fetchall()
                    for row in tab:
                        cross = {'dept':row[0], 'coursenum':row[1]}
                        table['deptcoursenums'].append(cross)
                    cursor.execute(''' SELECT area, title, descrip, prereqs
                                FROM courses
                                WHERE courseid = ?
                                ''', [courseid])
                    tab = cursor.fetchall()
                    for row in tab:
                        table['area'] = row[0]
                        table['title'] = row[1]
                        table['descrip'] = row[2]
                        table['prereqs'] = row[3]
                    cursor.execute(''' SELECT profname
                                FROM profs, coursesprofs
                                WHERE coursesprofs.profid = profs.profid
                                AND coursesprofs.courseid = ?
                                ORDER BY profname
                                ''', [courseid])
                    tab = cursor.fetchall()
                    for row in tab:
                        table['profnames'].append(row[0])
    return [success, table]
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
        print('Listening')
        while True:
            try:
                sock, _ = server_sock.accept()
                with sock:
                    print('Accepted connection, opened socket')
                    thread = CourseThread(sock)
                    thread.start()
                    thread.join()
                    
            except Exception as ex:
                print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
                sys.exit(1)
        
    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)



#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
