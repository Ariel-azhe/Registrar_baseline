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

    dept = flask.request.args.get('dept')
    coursenum = flask.request.args.get('coursenum')
    area = flask.request.args.get('area')
    title = flask.request.args.get('title')

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
                                      courses = courses, courseQuery = course)
    response = flask.make_response(html_code)

    # Set cookies
    response.set_cookie('dept', dept)
    response.set_cookie('coursenum', coursenum)
    response.set_cookie('area', area)
    response.set_cookie('title', title)

    return response

#-----------------------------------------------------------------------

# Page for class details and course details.
@app.route('/regdetails', methods=['GET'])
def reg_details():
    dept = flask.request.cookies.get('dept')
    coursenum = flask.request.cookies.get('coursenum')
    area = flask.request.cookies.get('area')
    title = flask.request.cookies.get('title')
    classid = flask.request.args.get('classid')

    if classid is None:
        classid = ''
    classid = classid.strip()

    details = database.search_details(classid)

    is_int = isinstance(classid, int)

    html_code = flask.render_template('regDetails.html',
                                      classid = classid,
                                      is_int = is_int,
                                      details = details,
                                      dept = dept,
                                      coursenum = coursenum,
                                      area = area,
                                      title = title)

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
