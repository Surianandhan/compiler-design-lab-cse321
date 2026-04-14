%{
#include <stdio.h>
#include "y.tab.h"
%}

alpha [A-Za-z_]
digit [0-9]

%%
[ \t\n]        ;
if             return IF;
then           return THEN;
else           return ELSE;
{digit}+       { yylval.num = atoi(yytext); return NUM; }
{alpha}({alpha}|{digit})* { yylval.id = strdup(yytext); return ID; }
"<="           return LE;
">="           return GE;
"=="           return EQ;
"!="           return NE;
"||"           return OR;
"&&"           return AND;
.              return yytext[0];
%%

int yywrap(void) {
    return 1;
}