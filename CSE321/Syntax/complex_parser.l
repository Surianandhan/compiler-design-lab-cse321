%{
#include <stdio.h>
#include "y.tab.h"
%}

alpha [A-Za-z]
digit [0-9]
whitespace [ \t\n]

%%
{whitespace}    ;
"if"            return IF;
"else"          return ELSE;
"return"        return RETURN;
"int"|"float"|"void"|"char" { yylval.type = strdup(yytext); return TYPE; }
{digit}+        { yylval.num = atoi(yytext); return NUM; }
{alpha}({alpha}|{digit})* { yylval.id = strdup(yytext); return ID; }
"=="            return EQ;
"!="            return NE;
"<="            return LE;
">="            return GE;
"&&"            return AND;
"||"            return OR;
"+"|"-"|"*"|"/"|"="|"<"|">"|"("|")"|"["|"]"|"{"|"}"|";"|"," { return yytext[0]; }
%%

int yywrap() {
    return 1;
}