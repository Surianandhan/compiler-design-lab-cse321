%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

extern int yylex();
%}

%union{
    int num;
    char *id;
    char *type;
}

%token TYPE RETURN IF ELSE
%token <num> NUM
%token <id> ID
%token <type> TYPE
%token EQ NE LE GE AND OR

%type <id> expression term factor arguments array_ref function_call

%%

program: 
       | program statement
       ;

statement: expression ';'
         | RETURN expression ';'
         | IF '(' expression ')' statement
         | IF '(' expression ')' statement ELSE statement
         | TYPE ID '=' expression ';'
         | TYPE ID '[' NUM ']' ';'
         ;

expression: term
          | expression '+' term
          | expression '-' term
          | expression '*' term
          | expression '/' term
          | expression EQ term
          | expression NE term
          | expression LE term
          | expression GE term
          | expression AND term
          | expression OR term
          | array_ref
          | function_call
          ;

term: factor
    | '(' expression ')'
    | '-' term
    ;

factor: ID
      | NUM
      | array_ref
      | function_call
      ;

array_ref: ID '[' expression ']'
         ;

function_call: ID '(' arguments ')'
             ;

arguments: /* empty */
         | expression
         | arguments ',' expression
         ;

%%

#include "lex.yy.c"

int main() {
    yyparse();
    return 0;
}