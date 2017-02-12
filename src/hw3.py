import sys
import lexer
import parser
import error


def main(filename):
    try:
        file_stream = open(filename, 'r')
        the_lexer = lexer.Lexer(file_stream)
        the_parser = parser.Parser(the_lexer)
        the_parser.parse()
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
