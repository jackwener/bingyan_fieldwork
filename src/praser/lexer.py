# -*- coding: utf-8 -*- 

import string
import operator

'''
'error2' #错误代码，字符串不封闭
'error3' #错误代码，数字以0开头
'error4' #错误代码，字符不封闭
'error5' #错误代码，浮点数中包含多个点，如1.2.3 
'error6' #错误代码，标识符中含有非法字符
'error7' #错误代码，数字和字母混合，如12AB56等
'''

_key = ("auto","break","case","char","const","continue","default",
"do","double","else","enum","extern","float","for",
"goto","if","int","long","register","return","short",
"signed","static","sizeof","struct","switch","typedef","union",
"unsigned","void","volatile","while")  # key word

_abnormalChar = '@#$%^&*~' # Illegal characters that may appear in the identifier

_syn = ''  # Type of word
_p = 0  # Subscript
_value = ''  # Store words analyzed by lexer
_content = ''  # Program code content
_mstate = 0  # finite state automata state of string
_cstate = 0  # finite state automata state of char
_dstate = 0  # finite state automata state of number
_line = 1  # Number of lines of code
_symbol = []  # Symbol table
ch = ''

# Save keywords and identifiers into the symbol table
def inSymbolTable(token):
    global _symbol
    if token not in _symbol:
        _symbol.append(token)


# get content from file
def get_code(contents):
    f = open(r'/home/jakevin/test.txt','r')
    for line in f:
        if line != '\n':
            contents = contents + line.lstrip()
        else:
            contents = contents + line
    f.close()
    return contents


# Clear the comment
def clear_comment(contents):
    state = 0  # finite state automata state
    index = -1  # Position index of characters
    
    for c in contents:
        index = index + 1
        
        if state == 0:
            if c == '/':
                state = 1
                startIndex = index
            
        elif state == 1:
            if c == '*':
                state = 2
            elif c == '/':
                # End of finite state automata
                comment = contents[startIndex:]
                contents = contents.replace(comment, '')
                index = startIndex - 1
                state = 0
            else:
                state = 0
                
        elif state == 2:
            if c == '*':
                state = 3
            else:
                pass
                
        elif state == 3:
            if c == '/':
                # End of finite state automata
                endIndex = index + 1
                comment = contents[startIndex:endIndex]
                contents = contents.replace(comment,'')
                index = startIndex - 1
                state = 0
                
            elif c == '*':
                pass
            else:
                state = 2
    return contents


def get_token(mystr, p, line):
    global _mstate, _dstate, _cstate, ch
    syn = ''
    val = ''
    lens = len(mystr)
    if p >= lens:
        syn = '#'
        return p, syn, val, line
    ch = mystr[p]
    p += 1
    while ch == ' ':
        ch = mystr[p]
        p += 1

    if ch in string.ascii_letters or ch == '_':  # letter(letter|digit)*
        while ch in string.ascii_letters or ch in string.digits or ch == '_' or ch in _abnormalChar:
            val += ch
            ch = mystr[p]
            p += 1
        p -= 1
        
        for abnormal in _abnormalChar:
            if abnormal in val:
                syn = 'error6' 
                break
            else:
                syn = 'ID'
        
        for s in _key:
            if operator.eq(s, val):
                syn = val.upper()               # key word
                break
        if syn == 'ID':
            inSymbolTable(val)
            
    elif ch == '\"':                        # string
        while ch in string.ascii_letters or ch in '\"% ':
            val += ch
            if _mstate == 0:
                if ch == '\"':
                    _mstate = 1
            elif _mstate == 1:
                if ch == '\"':
                    _mstate = 2

            ch = mystr[p]
            p += 1
            
        if _mstate == 1:
            syn = 'error2'     
            _mstate = 0
            
        elif _mstate == 2:
            _mstate = 0
            syn = 'STRING'
            
        p -= 1    
        
    elif ch in string.digits:
        while ch in string.digits or ch == '.' or ch in string.ascii_letters:
            val += ch
            if _dstate == 0:
                if ch == '0':
                    _dstate = 1
                else:
                    _dstate = 2
                    
            elif _dstate == 1:
                if ch == '.':
                    _dstate = 3
                else:
                    _dstate = 5
                    
            elif _dstate == 2:
                if ch == '.':
                    _dstate = 3
                
            ch = mystr[p]
            p += 1
        
        for char in string.ascii_letters:
            if char in val:
                syn = 'error7' 
                _dstate = 0
                
        if syn != 'error7':
            if _dstate == 5:
                syn = 'error3' 
                _dstate = 0
            else:    
                _dstate = 0
                if '.' not in val:
                    syn = 'INT'               # digit+
                else:
                    if val.count('.') == 1:
                        syn = 'FLOAT'           # Floating point number
                    else:
                        syn = 'error5'                
        p -= 1

    elif ch == '\'':  # char
        while ch in string.ascii_letters or ch in '@#$%&*\\\'\"':
            val += ch
            if _cstate == 0:
                if ch == '\'':
                    _cstate = 1
                    
            elif _cstate == 1:
                if ch == '\\':
                    _cstate = 2
                elif ch in string.ascii_letters or ch in '@#$%&*':
                    _cstate = 3
                    
            elif _cstate == 2:
                if ch in 'nt':
                    _cstate = 3
                    
            elif _cstate == 3:
                if ch == '\'':
                    _cstate = 4
            ch = mystr[p]
            p += 1
        
        p -= 1
        if _cstate == 4:
            syn = 'CHARACTER'
            _cstate = 0
        else:
            syn = 'error4'   
            _cstate = 0
                    
    elif ch == '<': 
        val = ch
        ch = mystr[p]
        
        if ch == '=':           # '<='
            val += ch
            p += 1
            syn = 'RELOP'
        else:                   # '<'
            syn = 'RELOP'
        
    elif ch == '>': 
        val = ch
        ch = mystr[p]
        
        if ch == '=':           # '>='
            val += ch
            p += 1
            syn = 'RELOP'
        else:                   # '>'
            syn = 'RELOP'
            
    elif ch == '!': 
        val = ch
        ch = mystr[p]
        
        if ch == '=':           # '!='
            val += ch
            p += 1
            syn = 'RELOP'
        else:                   # '!'
            syn = 'NOT'

    elif ch == '+': 
        val = ch
        ch = mystr[p]
        
        if ch == '+':            # '++'
            val += ch
            p += 1
            syn = '++'
        else:                  # '+'
            syn = 'PLUS'
        
    elif ch == '-': 
        val = ch
        ch = mystr[p]
        
        if ch == '-':            # '--'
            val += ch
            p += 1
            syn = '--'
        else:                  # '-'
            syn = 'MINUS'
            
    elif ch == '=':  
        val = ch
        ch = mystr[p]
        
        if ch == '=':            # '=='
            val += ch
            p += 1
            syn = 'RELOP'
        else:                  # '='
            syn = 'ASSIGNOP'
    
    elif ch == '&':
        val = ch 
        ch = mystr[p]
        
        if ch == '&':           # '&&'
            val += ch
            p += 1
            syn = 'AND'
        else:                   # '&'
            syn = '&'
            
    elif ch == '|':
        val = ch
        ch = mystr[p]
        
        if ch == '|':           # '||'       
            val += ch
            p += 1
            syn = 'OR'
        else:                   # '|'
            syn = '|'
    
    elif ch == '*':             # '*'
        val = ch
        syn = 'STAR'
        
    elif ch == '/':             # '/'
        val = ch
        syn = 'DIV'
        
    elif ch == ';':              # ';'
        val = ch
        syn = 'SEMI'
        
    elif ch == '(':             # '('
        val = ch
        syn = 'LP'
        
    elif ch == ')':             # ')'
        val = ch
        syn = 'RP'
        
    elif ch == '{':             # '{'
        val = ch
        syn = 'LC'
        
    elif ch == '}':             # '}'    
        val = ch
        syn = 'RC'       
        
    elif ch == '[':             # '['    
        val = ch
        syn = 'LB'   
        
    elif ch == ']':             # ']'    
        val = ch
        syn = 'RB'  
        
    elif ch == ',':             # ','    
        val = ch
        syn = 'COMMA'

    elif ch == '\n':
        line += 1
        p, syn, val, line = get_token(mystr, p, line)
    return p, syn, val, line