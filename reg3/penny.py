#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Ariel Yuan, Grace Best
#-----------------------------------------------------------------------

import html # html_code.escape() is used to thwart XSS attacks
import flask
import commons
import database
import parseargs

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    print("index")
    print(flask.request.args)

    dept = flask.request.args.get('department')
    print("dept is ", dept)
    coursenum = flask.request.args.get('course number')
    print("coursenum is ", coursenum)
    area = flask.request.args.get('area')
    print("area is ", area)
    title = flask.request.args.get('title')
    print("title is ", title)

    prev_dept = flask.request.cookies.get('prev_dept')
    prev_num = flask.request.cookies.get('prev_num')
    prev_area = flask.request.cookies.get('prev_area')
    prev_title = flask.request.cookies.get('prev_title')

    print(f"d: {prev_dept} | n: {prev_num} | a: {prev_area} | t: {prev_title}")

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
    

    course = {'dept': dept, 'coursenum':coursenum, 'area':area, 'title':title}
    print(course)
    
    courses = database.search_courses(course) # Exception handling omitted

    html_code = flask.render_template('index.html',
                                      courses =courses)

    response = flask.make_response(html_code)
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
    wresults = flask.request.args
    print(type(wresults))
    print((wresults.keys))
    #print(wresults[0])
    #print(wresults[1])
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
    print(f"classid: {classid}")
    print(results)
    details = results[1]
    print("details:", details)

    html_code = flask.render_template('regDetails.html',
        details = details)

    response = flask.make_response(html_code)
    return response


#-----------------------------------------------------------------------
def not_found():

    html_code = '''
        <!DOCTYPE html>
        <html>
            <head>
                <title>404 Not Found</title>
            </head>
            <body>
                <h1>Not Found</h1>
                <p>The requested URL was not found on the server.
                If you entered the URL manually please check your
                spelling and try again.</p>
            </body>
        </html>
        '''

    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
