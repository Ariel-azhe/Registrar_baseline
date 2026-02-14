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

#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite'

def main():
    try:
        with sqlite3.connect(DATABASE_URL + '?mode=ro',
            isolation_level=None, uri=True) as connection:

            with contextlib.closing(connection.cursor()) as cursor:
                reg_desc = ''.join(('Registrar application: ',
                                    'show details about a class'))
                classid_help = ''.join(('the id of the class whose ',
                                        'details should be shown'))
                parser = argparse.ArgumentParser(description = reg_desc)
                # Parse the command line argument as the classid
                parser.add_argument('classid', type = int,
                                    help = classid_help)
                ns = parser.parse_args()
                cursor.execute(f'''SELECT * FROM classes
                               WHERE classid = '{ns.classid}'
                               ''')
                table = cursor.fetchall()
                # If no corresponding class, exit with exit state 1
                if len(table) == 0:
                    print(''.join((f'{sys.argv[0]}: no class ',
                                   'with classid ',
                                   f'{ns.classid} exists')),
                                   file = sys.stderr)
                    sys.exit(1)
                print('-------------')
                print('Class Details')
                print('-------------')
                for row in table:
                    print('Class Id:', row[0])
                    # Store the class' courseid in a variable
                    courseid = row[1]
                    print('Days:', row[2])
                    print('Start time:', row[3])
                    print('End time:', row[4])
                    print('Building:', row[5])
                    print('Room:', row[6])
                print('--------------')
                print('Course Details')
                print('--------------')
                cursor.execute(f''' SELECT DISTINCT classes.courseid,
                               dept, coursenum
                               FROM classes, crosslistings
                               WHERE
                               classes.courseid = crosslistings.courseid
                               AND classes.courseid = '{courseid}'
                               ORDER BY dept, coursenum
                               ''')
                table = cursor.fetchall()
                printed = True
                for row in table:
                    if printed:
                        print('Course Id:', row[0])
                        printed = False
                    print('Dept and Number:', row[1], row[2])

                cursor.execute(f''' SELECT area, title, descrip, prereqs
                               FROM courses
                               WHERE courseid = '{courseid}'
                               ''')
                table = cursor.fetchall()
                space_num = 3
                for row in table:
                    if row[0] != '':
                        print('Area: ' + row[0])
                    else:
                        print('Area:')
                    for line in textwrap.wrap(
                        'Title: ' + row[1],
                        width = 72,
                        subsequent_indent= ' ' * space_num):
                        print(line)
                    for line in textwrap.wrap(
                        'Description: ' + row[2],
                        width = 72,
                        subsequent_indent= ' ' * space_num):
                        print(line)
                    for line in textwrap.wrap(
                        'Prerequisites: ' + row[3],
                        width = 72,
                        subsequent_indent=' ' * space_num):
                        print(line)
                cursor.execute(f''' SELECT profname
                               FROM profs, coursesprofs
                               WHERE coursesprofs.profid = profs.profid
                               AND coursesprofs.courseid = '{courseid}'
                               ORDER BY profname
                               ''')
                table = cursor.fetchall()
                for row in table:
                    print('Professor:', row[0])
    # Write the Exception message contained within
    # the thrown Exception object to stderr
    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
