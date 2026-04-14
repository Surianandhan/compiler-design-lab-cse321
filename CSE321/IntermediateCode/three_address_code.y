%{
#include <stdio.h>
#include <stdlib.h>
char temp = 'a';
%}

%union{
    int ival;
    char tvar;
}

%start statement
%token <ival> NUM
%type <tvar> E

%%

statement: E ';' { printf("\n"); }
         ;

E: NUM {
    $$ = temp++;
    printf("%c = %d\n", $$, $1);
   }
 | E '+' E {
    $$ = temp++;
    printf("%c = %c + %c\n", $$, $1, $3);
   }
 | E '-' E {
    $$ = temp++;
    printf("%c = %c - %c\n", $$, $1, $3);
   }
 | E '*' E {
    $$ = temp++;
    printf("%c = %c * %c\n", $$, $1, $3);
   }
 | E '/' E {
    $$ = temp++;
    printf("%c = %c / %c\n", $$, $1, $3);
   }
 | '(' E ')' {
    $$ = $2;
   }
 ;

%%

#include "lex.yy.c"

int main() {
    yyparse();
    return 0;
}

void yyerror(char *s) {
    fprintf(stderr, "Error: %s\n", s);
}