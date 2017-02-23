#!/usr/bin/python
"""
Author: Rudy Bermudez
Filename: hw4.py
Assignment: HW4
Description: Main Driver Class of Program
"""

import sys
import lexer
import parser
import error
import mypl_ast_printer as ast_printer


def main(filename):
    """ Opens a file and begins parsing the file.
    :param filename: The path of a file the user would like to parse
    :return: nothing if file is parsed without errors
    """
    try:
        file_stream = open(filename, 'r')
        the_lexer = lexer.Lexer(file_stream)
        the_parser = parser.Parser(the_lexer)
        stmt_list = the_parser.parse()
        print_visitor = ast_printer.ASTPrintVisitor(sys.stdout)
        stmt_list.accept(print_visitor)
    except IOError as e:
        print "error: unable to open file '" + filename + "'"
        sys.exit(1)
    except error.Error as e:
        print e
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage:', sys.argv[0], 'source - code - file'
        sys.exit(1)
    else:
        main(sys.argv[1])