#!/usr/bin/env python

#-----------------------------------------------------------------------
# regoverviews.py
# Author: Ariel Yuan, Grace Best
#-----------------------------------------------------------------------

import sys
import contextlib
import sqlite3
import argparse
import textwrap

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

def main():
    try:
        with sqlite3.connect(DATABASE_URL + '?mode=ro',
            isolation_level=None, uri=True) as connection:

            with contextlib.closing(connection.cursor()) as cursor:
                # Use argparse to parse arguments
                # and classify them into different options
                des = ''.join(('Registrar application: ',
                              'show overviews of classes'))
                dept_help = ''.join(('show only those classes ',
                                     'whose department '
                                     'contains dept'))
                num_help = ''.join(('show only those classes ',
                                    'whose course number ',
                                    'contains num'))
                area_help = ''.join(('show only those classes ',
                                     'whose distrib area ',
                                     'contains area'))
                title_help = ''.join(('show only those classes ',
                                      'whose course title ',
                                      'contains title'))
                ap = argparse.ArgumentParser(description = des)
                ap.add_argument('-d', type = str, metavar = 'dept',
                                help = dept_help)
                ap.add_argument('-n', metavar = 'num',
                                help = num_help)
                ap.add_argument('-a', type = str, metavar = 'area',
                                help = area_help)
                ap.add_argument('-t', metavar = 'title',
                                help = title_help)
                ns = ap.parse_args()

                # Select the columns that should be
                # displayed with corresponding courseids
                stmt_str = '''
                    SELECT classes.classid, crosslistings.dept, 
                    crosslistings.coursenum, courses.area, courses.title
                    FROM classes, crosslistings, courses
                    WHERE 
                    courses.courseid = classes.courseid and courses.courseid = crosslistings.courseid
                    '''
                # Adds constraints to the SQLite search
                # based on user input
                if ns.d:
                    stmt_str += f'''
                    AND dept = '{ns.d.upper()}' '''
                if ns.n:
                    stmt_str += f''' AND coursenum LIKE '%{ns.n}%' '''
                if ns.a:
                    stmt_str += f''' AND area = '{ns.a.upper()}' '''
                if ns.t:
                    stmt_str += f'''
                    AND title LIKE '%{escape_x(ns.t)}%' ESCAPE '/'
                    '''
                # Default case for no command line arguments:
                # display all classes
                if len(sys.argv) == 0:
                    stmt_str = '''
                    SELECT classes.classid, crosslistings.dept, 
                    crosslistings.coursenum, courses.area, courses.title
                    FROM classes, crosslistings, courses
                    '''
                stmt_str += 'ORDER BY dept, coursenum, classid'
                cursor.execute(stmt_str)
                table = cursor.fetchall()
                # Print output in specified table format
                print('ClsId', 'Dept', 'CrsNum', 'Area', 'Title')
                print('-----', '----', '------', '----', '-----')
                space_num = 5+1+4+1+6+1+4+1
                for row in table:
                    for line in textwrap.wrap('%5s %4s %6s %4s %s'
                                              % (row[0], row[1],
                                                 row[2], row[3],
                                                 row[4]),
                                              width = 72,
                                              subsequent_indent =
                                              ' ' * space_num):
                        print(line)
    # Write the Exception message contained within
    # the thrown Exception object to stderr
    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
