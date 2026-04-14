%{
#include <stdio.h>
#include <string.h>
#include "y.tab.h"
%}

%%
[0-9]+                { strcpy(yylval.var, yytext); return NAME; }
[a-z][a-z0-9]*        { strcpy(yylval.var, yytext); return NAME; }
"+"                   { return PLUS; }
"-"                   { return SUBT; }
"*"                   { return MULT; }
"/"                   { return DIVI; }
"="                   { return EQUAL; }
[ \t\n]               ;
.                     { return yytext[0]; }
%%

int yywrap() {
    return 1;
}