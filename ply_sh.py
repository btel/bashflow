#!/usr/bin/env python
#coding=utf-8

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

tokens = (
    'NAME','VAR', 
     'WORD',
     'SEP',
     'EXPORT',
    )

reserved = {
        'export' : 'EXPORT'
        }

# Tokens

t_VAR    = r'\$[a-zA-Z_][a-zA-Z0-9_]*'
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*='
    return t

def t_WORD(t):
    r'[^\s=\$]+'
    t.type = reserved.get(t.value, 'WORD')
    return t
    
t_SEP = r'[\s]+'


def t_COMMENT(t):
    r'\#.*'
    pass



# Ignored characters
t_ignore = "\t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

# dictionary of names
names = { }
env = {}

def p_statement_expr(t):
    'statement : expression'
    t[0] = {'cmd': t[1], 'env':env}

def p_export_statement(t):
    'statement : EXPORT SEP env'
    env.update(t[3])
    t[0] = {'cmd' : [], 'env' : env}

def p_statement_complex_expr(t):
    'statement : env expression'
    statement_env = env.copy()
    statement_env.update(t[1])
    t[0] = dict(cmd=t[2], env=statement_env)
     
def p_statement_env(t):
    'statement : env'
    names.update(t[1])
    t[0]= dict(cmd=[], env=[])

def p_env(t):
    'env : NAME word'
    t[0] = {t[1][:-1]:t[2]}

def p_env_sep(t):
    'env : env SEP'
    t[0] = t[1]

def p_env_empty(t):
    'env : NAME SEP'
    t[0] = {t[1][:-1]:''}


def p_expression_binop(t):
    '''expression : expression SEP expression'''
    t[0] = t[1] + t[3]

def p_expression_word(t):
    'expression : word'
    t[0] = [t[1]]

def p_word(t):
    '''word : WORD'''
    t[0] = t[1]

def p_expression_var(t):
    'word : VAR'
    try:
        t[0] = names[t[1][1:]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = '' 

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()
print __name__

if __name__ == '__main__':
    s = """abc=d
5+5+bAl
$abc * 2 + 5
"""

    lexer.input('abc=d')
    t = lexer.token()
    while t:
        print(t)
        t = lexer.token()


    for l in s.splitlines():
        print(l)
        print(parser.parse(l))
