%{
#include <stdio.h>
#include "y.tab.h"
%}

alpha [A-Za-z]
digit [0-9]

%%
[ \t\n]        ;
for            return FOR;
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

int yywrap() {
    return 1;
}