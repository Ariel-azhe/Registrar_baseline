#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Ariel Yuan, Grace Best
#-----------------------------------------------------------------------

import html # html_code.escape() is used to thwart XSS attacks
import http.cookies
import flask
import commons
import database
import parseargs

#-----------------------------------------------------------------------

app = flask.Flask(__name__)

#-----------------------------------------------------------------------

@app.route("/, methods=['GET']")
@app.route('/index', methods=['GET'])
def index(environ, start_response):
    print("index")

    args_str = environ.get('QUERY_STRING', '')
    print(args_str)
    args = parseargs.parse(args_str)
    print(args)
    course = args
    key = course.get("department")
    print("key is", key)

    # Dealing with empty input
    if key is None:
        prev_query = '(None)' # OG
        prev_dept = '(None)' # that was here b4 we implemented cookies
        courses = []
        print("courses none and is:")
        
    else: 
        prev_query = course # OG
        prev_dept = args['dept']
    
    prev_dept = flask.request.cookies.get('prev_dept')
    if prev_dept is None:
        prev_dept = '(None)'

    courses = database.search_courses(course) # Exception handling omitted

    html_code = flask.render_template('classSearch.html',
        head = commons.get_header(),
        foot = commons.get_footer(),
        listed_courses = convert_to_html(courses),
        prev_dept=prev_dept)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

def convert_to_html(courses):

    print("Entered convert")
    if len(courses) == 0:
        return '(None)'
    html_code = ''
    for course in courses:
        # print("length in courses")
        # print(courses)
        html_code += f'''
            <tr>
                <td><a href="/regdetails?classid={course['classid']}" </a>{course['classid']}</td> 
                <td>{html.escape(course['dept'])}</td> 
                <td>{(course['coursenum'])}</td>
                <td>{html.escape(course['area'])}</td> 
                <td>{html.escape(course['title'])}</td> 
            </tr>
            '''
    # print(html_code)
    return html_code

#-----------------------------------------------------------------------

def convert_to_html_details(details):

    print("Entered convert")
    if len(details) == 0:
        return '(None)'
    html_code = ''
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
def reg_details(environ, start_response):
    print("reg_details")
    args_str = environ.get('QUERY_STRING', '')
    args = parseargs.parse(args_str)
    classid = args.get('classid', '')
    classid = classid.strip()

    # fix later

    if classid == '':
        prev_query = '(None)' # OG
        details = []

    else:
        prev_query = classid # OG
        results = database.search_details(classid) # Exception handling omitted
        details = results[1]
        print("details:", details)

    html_code = f'''
        <!DOCTYPE html>
        <html>
            <head>
                <title>localhost:5001</title>
            </head>
            <body>
                {convert_to_html_details(details)}
                <hr>
                <p>Click here to do <a href="/">another class search</a></p>
                {commons.get_footer()}
            </body>
        </html>
        '''
    # print(html_code)
    content_header = ('content-type', 'text/html; charset=utf-8')
    headers = [content_header]
    start_response('200 OK', headers)
    prev_dept = flask.request.cookies.get('prev_dept')
    return [html_code.encode('utf-8')]


#-----------------------------------------------------------------------
def not_found(environ, start_response):

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

    content_header = ("content-type", "text/html; charset=utf-8")
    headers = [content_header]
    start_response("404 Not Found", headers)
    return [html_code.encode("utf-8")]

#-----------------------------------------------------------------------

def app(environ, start_response):
    print("Entered penny")
    path = environ.get('PATH_INFO', '').strip('/')
    
    if path in ('', 'index'):
        print("entered index")
        return index(environ, start_response)
    if path == 'regdetails':
        print("entered results")
        return reg_details(environ, start_response)
    

    return not_found(environ, start_response)