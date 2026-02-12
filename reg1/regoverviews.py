#!/usr/bin/env python

#-----------------------------------------------------------------------
# regoverviews.py
# Author: Ariel Yuan, Grace Best
#-----------------------------------------------------------------------

import sys
import random
import contextlib
import sqlite3
import argparse

#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite'

def process_x(x):
    x_list = list(x)
    subx = x
    index = subx.find("_")
    while index >= 0:
        x_list.insert(index, "~")
        subx = x[index + 1:]
        index = subx.find("_")

    new_x = "".join(x_list)
    subx = new_x
    x_list = list(new_x)
    index = subx.find("%")
    while index >= 0:
        x_list.insert(index, "~")
        subx = x[index + 1:]
        index = subx.find("%")


    new_x = "".join(x_list)
    return new_x

def main():

    try:
        with sqlite3.connect(DATABASE_URL + '?mode=ro',
            isolation_level=None, uri=True) as connection:

            with contextlib.closing(connection.cursor()) as cursor:

                # print the col names

                ap = argparse.ArgumentParser(description='regoverview')
                ap.add_argument('-d', nargs = 1)
                ap.add_argument('-n', nargs = 1)
                ap.add_argument('-a', nargs = 1)
                ap.add_argument('-t', nargs = '*')
                
                ns = ap.parse_args()

                stmt_str = f'''
                    SELECT classes.classid, crosslistings.dept, crosslistings.coursenum, courses.area, courses.title
                    FROM classes, crosslistings, courses
                    '''
                if ns.d:
                    stmt_str += f'''WHERE crosslistings.courseid = classes.courseid
                    AND dept = '{ns.d[0].upper()}' '''

                if ns.n:
                    if (stmt_str.find('WHERE') < 0):
                        stmt_str += f'''
                        WHERE crosslistings.courseid = classes.courseid
                        '''
                    stmt_str += f''' AND coursenum LIKE '%{ns.n[0].lower()}%' '''
                if ns.a:
                    if (stmt_str.find('WHERE') < 0):
                        stmt_str += f'''WHERE courses.courseid = classes.courseid
                    '''
                    else:
                        str_list = list(stmt_str)
                        str_list.insert(stmt_str.find('WHERE') + len('WHERE'), ' courses.courseid = classes.courseid and ')
                        stmt_str = "".join(str_list)

                    stmt_str += f''' AND area = '{ns.a[0].upper()}' '''
                if ns.t:
                    str = ""
                    for i in ns.t:
                        if i != '\"':
                            if i[1:].find('\"') > 0:
                                str += i[:len(i) - 1]
                            elif i[0:1] == '\"':
                                str += i[1:]
                            else:
                                str += i

                            if (i != ns.t[len(ns.t) - 1]):
                                str += " "
                    str = process_x(str.lower())
                    if (stmt_str.find('WHERE') < 0):
                        stmt_str += f'''
                        WHERE courses.courseid = classes.courseid
                    '''
                    elif stmt_str.find('courses.courseid = classes.courseid') < 0:
                        str_list = list(stmt_str)
                        str_list.insert(stmt_str.find('WHERE') + len('WHERE'), ' courses.courseid = classes.courseid and ')
                        stmt_str = "".join(str_list)

                    stmt_str += f'''
                    AND title LIKE '%{ns.t[0]}%' ESCAPE '~'
                    '''

                if len(sys.argv) == 0:
                    stmt_str = f'''
                    SELECT classes.classid, crosslistings.dept, crosslistings.coursenum, courses.area, courses.title
                    FROM classes, crosslistings, courses
                    '''

                print(stmt_str)
                cursor.execute(stmt_str)
                table = cursor.fetchall()
                for row in table:
                    print('%5s %4s %6s %4s %s' % (row[0], row[1], row[2], row[3], row[4]))

    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()

