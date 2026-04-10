#!/usr/bin/env python

#-----------------------------------------------------------------------
# registrar.py
# Author: Ariel Yuan, Grace Best
#-----------------------------------------------------------------------

import json
import flask
import database

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

# Main page. Default list all courses.
@app.route('/', methods=['GET'])
def index():
    return flask.send_file('index.html')

#-----------------------------------------------------------------------
@app.route('/searchresults', methods=['GET'])
def search_results():

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
              'area': area, 'title': title}

    courses = database.search_courses(course)
    
    # html_code = flask.send_file('index.html')
    json_doc = json.dumps(courses)
    response = flask.make_response(json_doc)
    
    #response.header['Conent-Type'] = 'application/json'
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

    # is_int = isinstance(classid, int)
    print("classid", classid)
    print("details", details)

    # html_code = flask.send_file('index.html')
    json_doc = json.dumps(details)
    response = flask.make_response(json_doc)
    print(response)
    #response.header['Conent-Type'] = 'application/json'
    return response

#-----------------------------------------------------------------------

# Page for faulty URL
@app.route('/notFound', methods=['GET'])
def not_found():

    html_code = flask.render_template('notFound.html')
    response = flask.make_response(html_code)

    return response

#-----------------------------------------------------------------------
