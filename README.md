# Reverse Descent Parser for MyPL Language

## Example MyPL Code
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
PRINT
RPAREN
STRING
PLUS
IF
NOT
GREATER THAN DO
PRINTLN
SEMICOLON
INT
MINUS
THEN
AND
LESS THAN EQUAL EOS
READINT
ID
BOOL
DIVIDE
ELSEIF
OR
GREATER THAN EQUAL
READSTR LBRACKET COMMA MULTIPLY ELSE EQUAL
NOT EQUAL
LPAREN
RBRACKET
ASSIGN
MODULUS
END
LESS THAN WHILE
```
