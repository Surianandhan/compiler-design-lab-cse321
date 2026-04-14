%{
#include <stdio.h>
int chars = 0;
int words = 0;
int lines = 0;
%}

%%
[a-zA-Z]+  { words++; chars += yyleng; }
\n         { lines++; chars++; }
.          { chars++; }
%%

int main() {
    yylex();
    printf("Lines: %d, Words: %d, Characters: %d\n", lines, words, chars);
    return 0;
}

int yywrap() {
    return 1;
}