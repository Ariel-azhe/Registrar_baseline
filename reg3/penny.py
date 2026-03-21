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

    dept = flask.request.args.get('dept')
    print("dept is ", dept)
    coursenum = flask.request.args.get('coursenum')
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

#-----------------------------------------------------------------------

def convert_to_html_details(details):

    print("Entered convert")
    if len(details) == 0:
        return '(None)'
    html_code = ''
        # print("length in courses")
        # print(courses)
    html_code += f'''
        {commons.get_header()}
        <hr>
        <h2> Class Details </h2>
        <table id="classDetailsTable" border = "1" cellpadding = "1" cellspacing = "2">
                <tr>
                    <td><strong>Class Id</strong></td>
                    <td>{details['classid']}</td>
                </tr>
                <tr>
                    <td><strong>Days</strong></td>
                    <td>{details['days']}</td>
                </tr>
                <tr>
                    <td><strong>Start time</strong></td>
                    <td>{details['starttime']}</td>
                </tr>
                <tr>
                    <td><strong>End time</strong></td>
                    <td>{details['endtime']}</td>
                </tr>
                <tr>
                    <td><strong>Building</strong></td>
                    <td>{details['bldg']}</td>
                </tr>
                <tr>
                    <td><strong>Room</strong></td>
                    <td>{details['roomnum']}</td>
                </tr>

            </table>
            <h2> Course Details </h2>
            <table id="courseDetailsTable" border = "1" cellpadding = "1" cellspacing = "2">
                <tr>
                    <td><strong>Course Id</strong></td>
                    <td>{details['courseid']}</td>
                </tr>
            '''
    for deptnum in details['deptcoursenums']:
        html_code += f'''
            <tr>
                <td><strong>Dept and Number</strong></td>
                <td>{deptnum['dept']} {deptnum['coursenum']}</td>
            </tr>
            '''
    html_code += f'''
        <tr>
            <td><strong>Area</strong></td>
            <td>{details['area']}</td>
        </tr>
        <tr>
            <td><strong>Title</strong></td>
            <td>{details['title']}</td>
        </tr>
        <tr>
            <td><strong>Description</strong></td>
            <td>{details['descrip']}</td>
        </tr>
        <tr>
            <td><strong>Prerequisites</strong></td>
            <td>{details['prereqs']}</td>
        </tr>
    '''
    for prof in details['profnames']:
        html_code += f'''
            <tr>
                <td><strong>Professor</strong></td>
                <td>{prof} </td>
            </tr>
            '''
    html_code += f'''
        </table>
    '''
    # print(html_code)
    return html_code

#-----------------------------------------------------------------------

@app.route('/regdetails', methods=['GET'])
def reg_details():
    print("reg_details")
    classid = flask.request.args.get('classid')
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
    details = results[1]
    print("details:", details)

    html_code = flask.render_template('regDetails.html',
        getDetails=convert_to_html_details(details))

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
