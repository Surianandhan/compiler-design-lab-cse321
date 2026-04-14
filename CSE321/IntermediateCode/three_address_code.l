%{
#include <stdio.h>
#include <stdlib.h>
#include "y.tab.h"
%}

%%
[0-9]+      { yylval.ival = atoi(yytext); return NUM; }
[ \t\n]     ;
.           { return yytext[0]; }
%%

int yywrap() {
    return 1;
}