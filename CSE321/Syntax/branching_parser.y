%{
#include <stdio.h>
#include <stdlib.h>
int yylex(void);
void yyerror(const char *s);
%}

%token ID NUM IF THEN ELSE LE GE EQ NE OR AND
%right '='
%left OR AND
%left '<' '>' LE GE EQ NE
%left '+' '-'
%left '*' '/'
%right UMINUS
%left '!'

%%

S : ST { printf("Input accepted.\n"); exit(0); }

ST : IF '(' E ')' ST ELSE ST
   | IF '(' E ')' ST
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
  | '(' E ')'
  | ID
  | NUM
  ;

%%

#include "lex.yy.c"

int main() {
    yyparse();
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}