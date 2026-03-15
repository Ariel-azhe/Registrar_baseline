#!/usr/bin/env python

#-----------------------------------------------------------------------
# parseargs.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import urllib.parse

#-----------------------------------------------------------------------

def _parse_help(arg_str):
    if '=' not in arg_str:
        name = urllib.parse.unquote_plus(arg_str)
        return (name, None)
    name, value = arg_str.split('=')
    name = urllib.parse.unquote_plus(name)
    value = urllib.parse.unquote_plus(value)
    return (name, value)

#-----------------------------------------------------------------------

def parse(args_str):
    args = {}
    arg_strs = args_str.split('&')
    for arg_str in arg_strs:
        name, value = _parse_help(arg_str)
        args[name] = value
    return args

#-----------------------------------------------------------------------

# For testing:

def _test():
    args_str = 'name1=value1&name2=value2&name+3=value+3&name4=&name5'
    args = parse(args_str)
    for name, value in args.items():
        print(name, ': ' , value)

if __name__ == '__main__':
    _test()
