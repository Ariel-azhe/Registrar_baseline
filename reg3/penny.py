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

app = flask.Flask(__name__)

#-----------------------------------------------------------------------

@app.route("/, methods=['GET']")
def index(environ, start_response):
    print("index")

    args_str = environ.get('QUERY_STRING', '')
    print(args_str)
    args = parseargs.parse(args_str)
    print(args)
    course = args
    print(course)
    key = course.get("department")
    print(key)

    if key is None:
        prev_author = '(None)'
        courses = []

    else: 
        print(len(course))
        prev_author = course
        courses = database.search_courses(course) # Exception handling omitted
    
    html_code = f'''
        <!DOCTYPE html>
        <html>
            <head>
                <title>localhost:5001</title>
            </head>
            <body>
                <h1>Registrar's Office</h1>
                <h2>Class Search</h2>
                <hr>
                <form action="/" method="get">
                    Dept:
                    <input type="text" name="department" id="deptInput" autofocus>
                    <br>
                    Number:
                    <input type="text" name = "course number" id="coursenumInput">
                    <br>
                    Area:
                    <input type="text" name = "area" id="areaInput">
                    <br>
                    Title:
                    <input type="text" name = "title" id="titleInput">
                    <br>
                    <input type="submit" id="submitButton" value="Go">
                </form>
                <table id="overviewsTable" border = "1" cellpadding = "1" cellspacing = "1">
                    <tr>
                        <th><strong>ClassId</strong></th>
                        <th><strong>Dept</strong></th>
                        <th><strong>Num</strong></th>
                        <th><strong>Area</strong></th>
                        <th><strong>Title</strong></th>
                    </tr>
                    {convert_to_html(courses)}
                    <tbody>

                    </tbody>
                </table>
                

                <br>
                {commons.get_footer()}
            </body>
        </html>
        '''
    print(html_code)

    content_header = ("content-type", "text/html; charset=utf-8")
    headers = [content_header]
    start_response("200 OK", headers)
    return [html_code.encode("utf-8")]

#-----------------------------------------------------------------------

def convert_to_html(courses):

    print("Entered convert")
    if len(courses) == 0:
        return '(None)'
    html_code = ''
    for course in courses:
        print("length in courses")
        print(courses)
        html_code += f'''
            console.log("hello")
            <tr>
                <td>{(course['classid'])}</td> 
                <td>{html.escape(course['dept'])}</td> 
                <td>{(course['coursenum'])}</td>
                <td>{html.escape(course['area'])}</td> 
                <td>{html.escape(course['title'])}</td> 
            </tr>
            '''
    print(html_code)
    return html_code

#-----------------------------------------------------------------------

@app.route('/searchresults', methods=['GET'])
def search_results(environ, start_response):
    print("search_results")
    args_str = environ.get('QUERY_STRING', '')
    args = parseargs.parse(args_str)
    course = args.get('course', '')
    print(course)
    course = course.strip()
    print(course)

    # fix later

    if course == '':
        prev_author = '(None)'
        courses = []

    else:
        prev_author = course
        courses = database.index(course) # Exception handling omitted

    html_code = f'''
        <!DOCTYPE html>
        <html>
            <head>
                <title>localhost:5001</title>
            </head>
            <body>
                {convert_to_html(courses)}
                {commons.get_footer()}
            </body>
        </html>
        '''
    print(html_code)
    content_header = ('content-type', 'text/html; charset=utf-8')
    #cookie = http.cookies.SimpleCookie()
    #cookie[’prev_author’] = prev_author
    #cookie_header = (’Set-Cookie’, cookie[’prev_author’].OutputString())
    #headers = [content_header, cookie_header]
    headers = [content_header]
    start_response('200 OK', headers)
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
    if path == 'searchresults':
        print("entered results")
        return search_results(environ, start_response)
    

    return not_found(environ, start_response)