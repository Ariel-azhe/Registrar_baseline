#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Ariel Yuan, Grace Best
#-----------------------------------------------------------------------

import flask
import database

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

# Main page. Default list all courses.
@app.route('/', methods=['GET'])
def index():

    dept = flask.request.args.get('department')
    coursenum = flask.request.args.get('course number')
    area = flask.request.args.get('area')
    title = flask.request.args.get('title')

    prev_dept = flask.request.cookies.get('prev_dept')
    prev_num = flask.request.cookies.get('prev_num')
    prev_area = flask.request.cookies.get('prev_area')
    prev_title = flask.request.cookies.get('prev_title')

    if prev_dept is None:
        prev_dept = ''
    if prev_num is None:
        prev_num = ''
    if prev_area is None:
        prev_area = ''
    if prev_title is None:
        prev_title = ''
    
    if (dept is None and coursenum is None
        and area is None and title is None):
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

    course = {'dept': dept, 'coursenum': coursenum,
              'area':area, 'title':title}

    courses = database.search_courses(course)

    html_code = flask.render_template('index.html',
                                      courses = courses)
    response = flask.make_response(html_code)

    # Set cookies
    response.set_cookie('prev_dept', dept)
    response.set_cookie('prev_num', coursenum)
    response.set_cookie('prev_area', area)
    response.set_cookie('prev_title', title)

    return response

#-----------------------------------------------------------------------

# Page for class details and course details.
@app.route('/regdetails', methods=['GET'])
def reg_details():
    classid = flask.request.args.get('classid')

    if classid is None:
        classid = ''
    classid = classid.strip()

    details = database.search_details(classid)

    is_int = isinstance(classid, int)

    html_code = flask.render_template('regDetails.html',
                                      classid = classid,
                                      is_int = is_int,
                                      details = details)

    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

# Page for faulty URL
@app.route('/notFound', methods=['GET'])
def not_found():

    html_code = flask.render_template('notFound.html')
    response = flask.make_response(html_code)

    return response

#-----------------------------------------------------------------------
