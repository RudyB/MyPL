# Recursive Descent Parser for MyPL Language

## Informal Description of MyPL Language
The language supports basic assignment statements, arithmetic expressions, conditionals, loops, lists, and basic input/output. All variables are implicitly typed (i.e., the types of variables are inferred from their values). Programs consist of a sequence of statements given within a single file.  

The language constructs supported by MyPL are described in more detail below.

1. **Primitive Data Types**
    > MyPL supports integer, string (denoted by double quotes, e.g., "Hello World!"), and Boolean values (true and false)
2. **List Types**
    > MyPL also supports Python-like lists. Lists are denoted by square brackets, e.g., “[1,2,3]”. List variables can be indexed, e.g., “xs[0]” to get the value in the first list position or to assign a value into the first list position.
3. **Assignment Statements**
    > An assignment statement takes the form “var = expr;” where var is a valid identifier (a letter followed by zero or more letters, digits, or underscores) and expr is a valid expression. Assignment statements bind the variable to the value that results from evaluating the expression. Assignment statements must end in a semicolon.
4. **Output Statements**
    > An output statement takes the form “print(expr);” or “println(expr);”. Print sends the value that results from evaluating the expression to standard output (the terminal). A println statement adds a newline to the result whereas a print statement does not. Print statements must end in a semicolon.
5. **Math Operators**
    > The typical math operators +, -, *, /, and % (modulus) are supported. Note that we only support integer division (e.g., the expression “5/2” evaluates to 2).
6. **Relational Operators**
    > The relational operators ==, <, >, <=, >=, and != are supported.
7. **Boolean Connectives**
    > The Boolean connectives and, or, and not are supported.
8. **Input Expressions**
    > User input is obtained through “readint(msg)” and “readstr(msg)” expressions, where “msg” is a string value. For example, “ans = readint("Enter an int: ")” prompts the user using the message “Enter an int: ”, and then after the user enters an integer value and hits “Enter”, the value is stored in the variable ans. A readint expression assumes an integer value is entered, whereas a readstr expression treats the input as a string value. Both readint and readstr expressions can occur anywhere an integer or string value would be used, respectively. For example, “println(5 + readint("Enter an int: "));” is a valid statement in MyPL.
9. **While Statements**
    > A while statement takes the form “while bool-expr do stmts end”, where bool-expr is a Boolean expression and stmts is a list of statements.
10. **Conditional Statements**
    > A condition statement takes the form “if bool-expr then stmts elseif bool-expr then stmts else stmts end”. A conditional statement can have zero or more elseif clauses and zero or one else clause. A conditional statement always ends with an “end” reserved word. Note that elseif is a distinct reserved word and should be used instead of an else followed by an if.
11. **Comments**
    > Single-line comments are denoted by the “#” symbol. That is, everything on a line after a “#” symbol is ignored.

## Example MyPL Program
The following are some simple examples of statements in MyPL:
```
# obligatory hello world program
println("Hello world!");


# simple conditional statement
x = readint("Enter an int: ");
y = readint("Enter an int: ");
if x > y then
    println("The first int was bigger than the second!");
elseif y > x then
    println("The second int was bigger than the first!");
else
    println("You entered the same value twice!");
end


# simple while statement
z = readint("Enter an int: ");
i = 0;
while z > 2 do
    z = z / 2;
    i = i + 1;
end
print("z = ");
print(z);
print(", i = ");
println(i);
```

## Valid Grammar
The MyPL language is based upon the following grammar:
```
<stmts> ::= <stmt> <stmts> | empty
<stmt> ::= <output> | <assign> | <cond> | <loop>
<output> ::= PRINT LPAREN <expr> RPAREN SEMICOLON | PRINTLN LPAREN <expr> RPAREN SEMICOLON
<input> ::= READINT LPAREN STRING RPAREN | READSTR LPAREN STRING RPAREN
<assign> ::= ID <listindex> ASSIGN <expr> SEMICOLON
<listindex> ::= LBRACKET <expr> RBRACKET | empty
<expr> ::= <value> <exprt>
<exprt> ::= <math_rel> <expr> | empty
<value> ::= ID <listindex> | STRING | INT | BOOL | <input> | LBRACKET <exprlist> RBRACKET
<exprlist> ::= <expr> <exprtail> | empty
<exprtail> ::= COMMA <expr> <exprtail> | empty
<math_rel> ::= PLUS | MINUS | DIVIDE | MULTIPLY | MODULUS
<cond> ::= IF <bexpr> THEN <stmts> <condt> END
<condt> ::= ELSEIF <bexpr> THEN <stmts> <condt> | ELSE <stmts> | empty
<bexpr> ::= <expr> <bexprt> | NOT <expr> <bexprt>
<bexprt> ::= <bool_rel> <expr> <bconnct> | empty
<bconnct> ::= AND <bexpr> | OR <bexpr> | empty
<bool_rel> ::= EQUAL | LESS_THAN | GREATER_THAN | LESS_THAN_EQUAL | GREATER_THAN_EQUAL | NOT_EQUAL
<loop> ::= WHILE <bexpr> DO <stmts> END
```

## Valid Tokens
```
STRING
INT
BOOL
PRINT
PRINTLN
READINT
READSTR
PLUS
MINUS
MULTIPLY
DIVIDE
MODULUS
AND
NOT
OR
ID
ASSIGN
SEMICOLON
LBRACKET
RBRACKET
COMMA
LPAREN
RPAREN
IF
THEN
ELSEIF
ELSE
EQUAL
NOT EQUAL
LESS THAN
LESS THAN EQUAL
GREATER THAN
GREATER THAN EQUAL
WHILE
DO
END
EOS
```
## Running the application
The program takes a source file written in MyPL and outputs an Abstract Syntax Tree (AST).

The application can be started with:  
```bash
python hw4.py exampleMyPLProgram.txt
```

## Example Output
```
StmtList:
  AssignStmt:
    ID: xs
    ListExpr:
      SimpleExpr: INT (1)
      SimpleExpr: INT (2)
      SimpleExpr: INT (3)
      SimpleExpr: INT (4)
      SimpleExpr: INT (5)
  AssignStmt:
    ID: ys
    ListExpr:
      SimpleExpr: INT (10)
      SimpleExpr: INT (20)
      SimpleExpr: INT (30)
      SimpleExpr: INT (40)
      SimpleExpr: INT (50)
  AssignStmt:
    ID: i
    SimpleExpr: INT (0)
  WhileStmt:
    CONDITION:
      ComplexBoolExpr:
        SimpleExpr: ID (i)
        LESS_THAN
        SimpleExpr: INT (5)
    BODY:
      StmtList:
        AssignStmt:
          INDEXED ID: xs
          SimpleExpr: ID (i)
          IndexExpr:
            INDEXED ID (ys)
            SimpleExpr: ID (i)
        AssignStmt:
          INDEXED ID: xs
          ComplexExpr:
            SimpleExpr: ID (i)
            PLUS
            SimpleExpr: INT (1)
          ComplexExpr:
            IndexExpr:
              INDEXED ID (xs)
              SimpleExpr: ID (i)
            PLUS
            ComplexExpr:
              IndexExpr:
                INDEXED ID (y)
                SimpleExpr: ID (i)
              MULTIPLY
              SimpleExpr: INT (2)
        AssignStmt:
          ID: i
          ComplexExpr:
            SimpleExpr: ID (i)
            PLUS
            SimpleExpr: INT (1)
  PrintStmt: PRINT
    SimpleExpr: STRING (xs: )
  PrintStmt: PRINTLN
    SimpleExpr: ID (xs)
  AssignStmt:
    ID: halt
    SimpleExpr: BOOL (false)
  WhileStmt:
    CONDITION:
      SimpleBoolExpr:
        NOT
        SimpleExpr: ID (halt)

    BODY:
      StmtList:
        AssignStmt:
          ID: ans
          ReadExpr: READSTR (Type y to continue: )
        IfStmt:
          IF:
            ComplexBoolExpr:
              SimpleExpr: ID (ans)
              EQUAL
              SimpleExpr: STRING (y)
          THEN:
            StmtList:
              AssignStmt:
                ID: halt
                SimpleExpr: BOOL (true)
```

## License   
This repository is released under the MIT license. See LICENSE for details.
