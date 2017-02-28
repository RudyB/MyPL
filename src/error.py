"""
Author: Rudy Bermudez
Filename: error.py
Assignment: HW5
Description: Model an Error
"""


class Error(Exception):
    """ Model class of an Error
    :Parameters:
        - message: The issue that caused the error
        - line: line where error occurred
        - column: column where error occurred
    """

    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        s = ''
        s += 'error: ' + self.message
        s += ' at line ' + str(self.line)
        s += ' column ' + str(self.column)
        return s
