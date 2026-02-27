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

def write_class(details):
    print('-------------')
    print('Class Details')
    print('-------------')
    print('Class Id:', details['classid'])
    # Store the class' courseid in a variable
    courseid = details['courseid']
    print('Days:', details['days'])
    print('Start time:', details['starttime'])
    print('End time:', details['endtime'])
    print('Building:', details['bldg'])
    print('Room:', details['roomnum'])
    print('--------------')
    print('Course Details')
    print('--------------')
    cursor.execute(''' SELECT DISTINCT classes.courseid,
                               dept, coursenum
                               FROM classes, crosslistings
                               WHERE
                               classes.courseid = crosslistings.courseid
                               AND classes.courseid = ?
                               ORDER BY dept, coursenum
                               ''', [courseid])
    table = cursor.fetchall()
    print('Course Id:', details['courseid'])
    for cross in details['deptcoursenums']:
        print('Dept and Number:', cross['dept'], cross['coursenum'])
    if details['area'] != '':
        print('Area: ' + details['area'])
    else:
        print('Area:')
    for line in textwrap.wrap(
        'Title: ' + details['title'],
        width = 72,
        subsequent_indent= ' ' * space_num):
        print(line)
    for line in textwrap.wrap(
        'Description: ' + details['descrip'],
        width = 72,
        subsequent_indent= ' ' * space_num):
        print(line)
    for line in textwrap.wrap(
        'Prerequisites: ' + details['prereqs'],
        width = 72,
        subsequent_indent=' ' * space_num):
        print(line)

    for prof in details['profnames']:
        print('Professor:', prof)

    for row in table:
        if printed:
            print('Course Id:', row[0])
            printed = False
        print('Dept and Number:', row[1], row[2])

    cursor.execute(''' SELECT area, title, descrip, prereqs
                               FROM courses
                               WHERE courseid = ?
                               ''', [courseid])
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
    cursor.execute(''' SELECT profname
                               FROM profs, coursesprofs
                               WHERE coursesprofs.profid = profs.profid
                               AND coursesprofs.courseid = ?
                               ORDER BY profname
                               ''', [courseid])
    table = cursor.fetchall()
    for row in table:
        print('Professor:', row[0])
def main():
    try:
        reg_desc = ''.join(('Registrar application: ',
                            'show details about a class'))
        classid_help = ''.join(('the id of the class whose ',
                                'details should be shown'))
        parser = argparse.ArgumentParser(description = reg_desc)
        # Parse the command line argument as the classid
        parser.add_argument('classid', type = int,
                            help = classid_help)
        ns = parser.parse_args()
                
    # Write the Exception message contained within
    # the thrown Exception object to stderr
    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
