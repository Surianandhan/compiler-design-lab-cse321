# Compiler Design Lab

This repository contains implementations of various compiler design concepts using LEX, YACC, C/C++, and Python.

## Topics Covered

### Lexical Analysis
- Word, line, character counter using LEX
- Token recognition for C programs

### Syntax Analysis
- Parser for branching statements (if-else)
- Parser for looping statements (for loops)
- Parser for complex C constructs (arrays, functions)

### Grammar Analysis
- FIRST and FOLLOW set computation
- LL(1) parsing table construction

### Parsing Techniques
- LR(1) parser implementation

### Intermediate Code Generation
- Three-address code generation
- Infix to postfix conversion

### Code Generation
- Intermediate code to assembly-like instructions

### Code Optimization
- Common Subexpression Elimination
- Peephole Optimization

### Register Allocation
- Liveness analysis
- Interference graph
- Graph coloring

## Tools Used
- LEX & YACC
- C / C++
- Python

## How to Run

### LEX Programs
lex file.l
gcc lex.yy.c
./a.out

### LEX + YACC Programs
lex file.l
yacc file.y
gcc y.tab.c -ll -ly
./a.out

### Python Programs
python3 file.py

## Author
Surianandhan Sridhar
