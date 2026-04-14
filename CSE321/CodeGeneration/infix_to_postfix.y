%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
%}

%union {
    char *sval;
}

%token <sval> ID
%left '+' '-'
%left '*' '/'
%right UMINUS

%%

S: E '\n' { printf("\n"); }
 ;

E: E '+' E { push("+"); pop(); }
 | E '-' E { push("-"); pop(); }
 | E '*' E { push("*"); pop(); }
 | E '/' E { push("/"); pop(); }
 | '(' E ')'
 | '-' E   { push("~"); pop(); }
 | ID      { printf("%s", $1); free($1); }
 ;

%%

#include "lex.yy.c"
char *stack[100];
int top = 0;

void push(char *op) {
    stack[top++] = op;
}

void pop() {
    printf("%s", stack[--top]);
}

int main() {
    printf("Enter infix expression: ");
    yyparse();
    return 0;
}

void yyerror(char *s) {
    fprintf(stderr, "Error: %s\n", s);
}