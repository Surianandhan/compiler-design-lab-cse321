%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
%}

%union{
    int num;
    char *id;
}

%token ID NUM FOR LE GE EQ NE OR AND
%right '='
%left OR AND
%left '<' '>' LE GE EQ NE
%left '+' '-'
%left '*' '/'
%right UMINUS
%left '!'

%%

S : ST { printf("Input accepted\n"); exit(0); }

ST : FOR '(' E ';' E ';' E ')' DEF

DEF : BODY
    | E ';' ST
    ;

BODY : BODY BODY
     | E ';'
     ;

E : ID '=' E
  | E '+' E
  | E '-' E
  | E '*' E
  | E '/' E
  | E '<' E
  | E '>' E
  | E LE E
  | E GE E
  | E EQ E
  | E NE E
  | E OR E
  | E AND E
  | ID '+' '+'
  | ID '-' '-'
  | '+' '+' ID
  | '-' '-' ID
  | '(' E ')'
  | ID
  | NUM
  ;

%%

#include "lex.yy.c"

int main() {
    printf("Enter the expression:\n");
    yyparse();
    return 0;
}

void yyerror(char *s) {
    fprintf(stderr, "Error: %s\n", s);
}