%{
#include <stdio.h>
#include <string.h>
%}

%union {
    char var[50];
}

%token <var> NAME
%token PLUS SUBT MULT DIVI EQUAL
%type <var> exp
%right EQUAL
%left PLUS SUBT
%left MULT DIVI

%%

input: line '\n' input
     | '\n' input
     |
     ;

line: NAME EQUAL exp { printf("STA %s\n", $1); }
    ;

exp: exp PLUS exp  { printf("LDA %s\nLDT %s\nADDR A,T\n", $1, $3); strcpy($$, $1); }
   | exp SUBT exp  { printf("LDA %s\nLDT %s\nSUBR A,T\n", $1, $3); strcpy($$, $1); }
   | exp MULT exp  { printf("LDA %s\nLDT %s\nMULR A,T\n", $1, $3); strcpy($$, $1); }
   | exp DIVI exp  { printf("LDA %s\nLDT %s\nDIVR A,T\n", $1, $3); strcpy($$, $1); }
   | '(' exp ')'   { strcpy($$, $2); }
   | NAME          { strcpy($$, $1); }
   ;

%%

#include "lex.yy.c"

int main() {
    yyparse();
    return 0;
}

void yyerror(char *s) {
    printf("Error: %s\n", s);
}