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

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index(environ, start_response):

    html_code = f'''
        <!DOCTYPE html>
        <html>
            <head>
                <title>localhost:5001.com</title>
            </head>
            <body>
                Click to <a href="/searchcourses">begin</a>.<br>
                <br>
                {commons.get_footer()}
            </body>
        </html>
        '''

    content_header = ("content-type", "text/html; charset=utf-8")
    headers = [content_header]
    start_response("200 OK", headers)
    return [html_code.encode("utf-8")]

#-----------------------------------------------------------------------

@app.route("/searchcourses, methods=['GET']")
def search_courses(environ, start_response):
    print("hello")
    
    html_code = f'''
        console.log("hello")
        <!DOCTYPE html>
        <html>
            <head>
                <title>localhost:5001.com</title>
            </head>
            <body>
                <h1>Registrar's Office</h1>
                <h2>Class Search</h2>
                <hr>
                <form action="/searchcourses" method="get">
                    Dept:
                    <input type="text" name="deptInput" autofocus>
                    Number:
                    <input type="text" name="coursenumInput" autofocus>
                    Area:
                    <input type="text" name="areaInput" autofocus>
                    Title:
                    <input type="text" name="titleInput" autofocus>
                    <input type="submit" name="submitButton" value="Go">
                </form>
                <br>
                {commons.get_footer()}
            </body>
        </html>
        '''

    content_header = ("content-type", "text/html; charset=utf-8")
    headers = [content_header]
    start_response("200 OK", headers)
    return [html_code.encode("utf-8")]

#-----------------------------------------------------------------------

def convert_to_html(courses):

    if len(courses) == 0:
        return '(None)'
    html_code = ''
    for course in courses:
        html_code += f'''
            <strong>{html.escape(course['dept'])}</strong>:
            {html.escape(course['coursenum'])}:
            {html.escape(course['area'])}
            {html.escape(course['title'])}<br>
            '''
    return html_code

#-----------------------------------------------------------------------

@app.route('/searchresults', methods=['GET'])
def search_results(environ, start_response):

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
        courses = database.search_courses(course) # Exception handling omitted

    html_code = f'''
        <!DOCTYPE html>
        <html>
            <head>
                <title>localhost:5001.com</title>
            </head>
            <body>
                {convert_to_html(courses)}
                {commons.get_footer()}
            </body>
        </html>
        '''

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
        return index(environ, start_response)
    if path == 'searchresults':
        return search_results(environ, start_response)
    if path == 'searchcourses':
        return search_courses(environ, start_response)
    
    

    return not_found(environ, start_response)