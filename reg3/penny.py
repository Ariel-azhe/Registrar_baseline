#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Ariel Yuan, Grace Best
#-----------------------------------------------------------------------

import html # html_code.escape() is used to thwart XSS attacks
import flask
import database

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    print("index")
    print(flask.request.args)

    dept = flask.request.args.get('department')
    coursenum = flask.request.args.get('course number')
    area = flask.request.args.get('area')
    title = flask.request.args.get('title')
    print(f"d is: {dept} | n is: {coursenum} | a is: {area} | t is: {title}")

    prev_dept = flask.request.cookies.get('prev_dept')
    prev_num = flask.request.cookies.get('prev_num')
    prev_area = flask.request.cookies.get('prev_area')
    prev_title = flask.request.cookies.get('prev_title')

    print(f"d prev: {prev_dept} | n prev: {prev_num} | a prev: {prev_area} | t prev: {prev_title}")

    if prev_dept is None:
        prev_dept = ''
    if prev_num is None:
        prev_num = ''
    if prev_area is None:
        prev_area = ''
    if prev_title is None:
        prev_title = ''
    if dept is None and coursenum is None and area is None and title is None:
        print("all none")
        dept = prev_dept
        coursenum = prev_num
        area = prev_area
        title = prev_title
    else:
        if dept is None:
            dept = ''
        dept = dept.strip()
        
        if coursenum is None:
            coursenum = ''
        coursenum = coursenum.strip()
        
        if area is None:
            area = ''
        area = area.strip()
        
        if title is None:
            title = ''
        title = title.strip()
    

    course = {'dept': dept, 'coursenum': coursenum, 'area':area, 'title':title}
    print(course)
    
    courses = database.search_courses(course) # Exception handling omitted

    html_code = flask.render_template('index.html',
                                      courses =courses)

    response = flask.make_response(html_code)

    # Set cookies
    response.set_cookie('prev_dept', dept)
    response.set_cookie('prev_num', coursenum)
    response.set_cookie('prev_area', area)
    response.set_cookie('prev_title', title)

    return response


#-----------------------------------------------------------------------

@app.route('/regdetails', methods=['GET'])
def reg_details():
    print("reg_details")
    classid = flask.request.args.get('classid')
    print(flask.request.args)
    print(f"classid 1: {classid}")

    if classid is None:
        classid = ''
    classid = classid.strip()

    # fix later
    prev_dept = flask.request.cookies.get('prev_dept')
    prev_num = flask.request.cookies.get('prev_num')
    prev_area = flask.request.cookies.get('prev_area')
    prev_title = flask.request.cookies.get('prev_title')
    prev_query_str = f'?dept={prev_dept}&coursenum={prev_num}&area={prev_area}&title={prev_title}'

    results = database.search_details(classid) # Exception handling omitted
    print(f"classid 2: {classid}")
    print(results)
    exists = results[0]
    print(results[0])
    details = results[1]
    print("details:", details)

    isInt = True
    if (type(classid) != int):
        isInt = False

    html_code = flask.render_template('regDetails.html', 
                                      exists = exists,
                                      classid = classid,
                                      isInt = isInt,
                                      details = details)

    response = flask.make_response(html_code)
    return response


#-----------------------------------------------------------------------

@app.route('/notFound', methods=['GET'])
def not_found():

    html_code = flask.render_template('notFound.html')
    response = flask.make_response(html_code)

    return response

#-----------------------------------------------------------------------
