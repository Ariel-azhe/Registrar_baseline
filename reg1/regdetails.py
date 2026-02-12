#!/usr/bin/env python

#-----------------------------------------------------------------------
# display.py
# Author: Ariel Yuan, Grace Best
#-----------------------------------------------------------------------

import sys
import contextlib
import sqlite3
import textwrap

#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite'

def main():

    if len(sys.argv) != 2:
        print(f'usage: python {sys.argv[0]}', file=sys.stderr)
        sys.exit(1)

    try:
        with sqlite3.connect(DATABASE_URL + '?mode=ro',
            isolation_level=None, uri=True) as connection:

            with contextlib.closing(connection.cursor()) as cursor:
                classnum = sys.argv[1]
                print('-------------------------------------------')
                print('Class Details')
                print('-------------------------------------------')
                cursor.execute(f'''SELECT * FROM classes WHERE classid = '{classnum}' 
                               ''')
                table = cursor.fetchall()
                for row in table:
                    print('Class Id:', row[0])
                    courseid = row[1]
                    print('Days:', row[2])
                    print('Start time:', row[3])
                    print('End time:', row[4])
                    print('Building:', row[5])
                    print('Room:', row[6])

                print('-------------------------------------------')
                print('Course Details')
                print('-------------------------------------------')
                cursor.execute(f''' SELECT DISTINCT classes.courseid, dept, coursenum
                               FROM classes, crosslistings
                               WHERE classes.courseid = crosslistings.courseid
                               AND classes.courseid = '{courseid}'
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
                for row in table:
                    print('Area:', row[0])
                    for line in textwrap.wrap('Title: ' + row[1], width = 72, subsequent_indent= '   '):
                        print(line)
                    for line in textwrap.wrap('Descriptions: ' + row[2], width = 72, subsequent_indent= '   '):
                        print(line)
                    for line in textwrap.wrap('Prerequisites: ' + row[3], width = 72, subsequent_indent= '   '):
                        print(line)
                cursor.execute(f''' SELECT profname
                               FROM profs, coursesprofs
                               WHERE coursesprofs.profid = profs.profid
                               AND coursesprofs.courseid = '{courseid}'
                               ''')
                table = cursor.fetchall()
                for row in table:
                    print('Professor:', row[0])

    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()