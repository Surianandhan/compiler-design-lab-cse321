%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "y.tab.h"
%}

ALPHA [A-Za-z]
DIGIT [0-9]

%%
{ALPHA}({ALPHA}|{DIGIT})* { yylval.sval = strdup(yytext); return ID; }
{DIGIT}+                   { yylval.sval = strdup(yytext); return ID; }
[ \t\n]                    ;
.                          { return yytext[0]; }
%%

int yywrap() {
    return 1;
}