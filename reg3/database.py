#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Ariel Yuan, Grace Best
#-----------------------------------------------------------------------

import sys
import sqlite3
import contextlib

#-----------------------------------------------------------------------

_DATABASE_URL = 'file:reg.sqlite'

#-----------------------------------------------------------------------

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

#-----------------------------------------------------------------------

# Function to access the database
# And search for class details to be
# Returned to and displayed by 
# The regdetails.py client
def search_details(args):
    success = True
    with sqlite3.connect(_DATABASE_URL + '?mode=ro',
            isolation_level=None, uri=True) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            classid = args
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
            cursor.execute('''SELECT * FROM classes
                            WHERE classid = ?
                            ''', [classid])
            tab = cursor.fetchall()
            if len(tab) == 0:
                success = False
                table = ''.join((f'{sys.argv[0]}: ',
                                'no class with classid ',
                                f'{classid} exists'))
            else:
                for row in tab:
                    table['classid'] = row[0]
                    table['courseid'] = row[1]
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
                            ''', [table['courseid']])
                tab = cursor.fetchall()
                for row in tab:
                    cross = {'dept':row[0], 'coursenum':row[1]}
                    table['deptcoursenums'].append(cross)
                cursor.execute('''
                                SELECT area, title, descrip, prereqs
                                FROM courses
                                WHERE courseid = ?
                                ''', [table['courseid']])
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
                            ''', [table['courseid']])
                tab = cursor.fetchall()
                for row in tab:
                    table['profnames'].append(row[0])
    return [success, table]

#-----------------------------------------------------------------------

# Function to access the database
# And search for courses to be
# Returned to and displayed by 
# The regoverviews.py client
def search_courses(args):
    with sqlite3.connect(_DATABASE_URL + '?mode=ro',
            isolation_level=None, uri=True) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            dict = args
            print("print args below?")
            print(f"this is args?: {args}")

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
            if len(args) == 4:
                if dict['department'] != '':
                    stmt_str += ' AND crosslistings.dept LIKE ? '
                    prepare.append(f'%{dict['department'].upper()}%')
                if dict['course number'] != '':
                    stmt_str += ' AND coursenum LIKE ? '
                    prepare.append(f'%{dict['course number']}%')
                if dict['area'] != '':
                    stmt_str += ' AND area LIKE ? '
                    prepare.append(f'%{dict['area'].upper()}%')
                if dict['title'] != '':
                    stmt_str += '''
                    AND title LIKE ? ESCAPE '/'
                    '''
                    prepare.append(f'%{escape_x(dict['title'])}%')

            stmt_str += 'ORDER BY dept, coursenum, classid'
            print(stmt_str)
            cursor.execute(stmt_str, prepare)
            tab = cursor.fetchall()
            table = []
            for cls in tab:
                dict = {'classid': cls[0],
                        'dept': cls[1],
                        'coursenum':cls[2],
                        'area': cls[3],
                        'title': cls[4]}
                table.append(dict)
    return table

#-----------------------------------------------------------------------
