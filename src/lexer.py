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

_abnormalChar = '@#$%^&*~' #Illegal characters that may appear in the identifier

_syn = ''  #Type of word
_p = 0  #Subscript
_value = ''  #Store words analyzed by lexer
_content = '' #Program code content
_mstate = 0 #finite state automata state of string
_cstate = 0 #finite state automata state of char
_dstate = 0 #finite state automata state of number
_line = 1 #Number of lines of code
_symbol = [] #Symbol table

# Save keywords and identifiers into the symbol table
def inSymbolTable(token):
    global _symbol
    if token not in _symbol:
        _symbol.append(token)

# get content from file
def getCode():
    global _content
    f = open(r'/home/jakevin/test.txt','r')
    for line in f:
        if line != '\n':
            _content = _content+line.lstrip() 
        else:
            _content = _content+line
    f.close()

# Clear the comment
def clearComment():
    global _content
    state = 0 #finite state automata state
    index = -1 #Position index of characters
    
    for c in _content:
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
                comment = _content[startIndex:]
                _content = _content.replace(comment,'') 
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
                comment = _content[startIndex:endIndex]
                _content = _content.replace(comment,'') 
                index = startIndex - 1
                state = 0
                
            elif c == '*':
                pass
            else:
                state = 2

def getToken(mystr):
    global _p,_value,_syn,_mstate,_dstate,_line,_cstate
    
    _value = ''
    ch = mystr[_p]
    _p += 1
    while ch == ' ':
        ch = mystr[_p]
        _p += 1


    if ch in string.ascii_letters or ch == '_':    # letter(letter|digit)*
        while ch in string.ascii_letters or ch in string.digits or ch == '_' or ch in _abnormalChar:
            _value += ch
            ch = mystr[_p]
            _p += 1
        _p -= 1
        
        for abnormal in _abnormalChar:
            if abnormal in _value:
                _syn = 'error6' 
                break
            else:
                _syn = 'ID'
        
        for s in _key:
            if operator.eq(s,_value) == True:
                _syn = _value.upper()               # key word
                break
        if _syn == 'ID':
            inSymbolTable(_value)
            
    elif ch == '\"':                        # string
        while ch in string.ascii_letters or ch in '\"% ' :
            _value += ch
            if _mstate == 0:
                if ch == '\"':
                    _mstate = 1
            elif _mstate == 1:
                if ch == '\"':
                    _mstate = 2

            ch = mystr[_p]
            _p += 1
            
        if _mstate == 1:
            _syn = 'error2'     
            _mstate = 0
            
        elif _mstate == 2:
            _mstate = 0
            _syn = 'STRING'
            
        _p -= 1    
        
    elif ch in string.digits:
        while ch in string.digits or ch == '.' or ch in string.ascii_letters:
            _value += ch
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
                
            ch = mystr[_p]
            _p += 1
        
        for char in string.ascii_letters:
            if char in _value:
                _syn = 'error7' 
                _dstate = 0
                
                
        if _syn != 'error7':
            if _dstate == 5:
                _syn = 'error3' 
                _dstate = 0
            else:    
                _dstate = 0
                if '.' not in _value:
                    _syn = 'DIGIT'               # digit+
                else:
                    if _value.count('.') == 1:
                        _syn = 'FRACTION'           # Floating point number 
                    else:
                        _syn = 'error5'                
        _p -= 1
            
                
    elif ch == '\'':                    # char
        while ch in string.ascii_letters or ch in '@#$%&*\\\'\"':
            _value += ch
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
            ch = mystr[_p]
            _p += 1
        
        _p -= 1
        if _cstate == 4:
            _syn = 'CHARACTER'
            _cstate = 0
        else:
            _syn = 'error4'   
            _cstate = 0
                    
    elif ch == '<': 
        _value = ch
        ch = mystr[_p]
        
        if ch == '=':           #  '<='
            _value += ch
            _p += 1
            _syn = '<='
        else:                   # '<'
            _syn = '<'
        
    elif ch == '>': 
        _value = ch
        ch = mystr[_p]
        
        if ch == '=':           #'>='
            _value += ch
            _p += 1
            _syn = '>='
        else:                   # '>'
            _syn = '>'
            
    elif ch == '!': 
        _value = ch
        ch = mystr[_p]
        
        if ch == '=':           #'!='
            _value += ch
            _p += 1
            _syn = '!='
        else:                   # '!'
            _syn = 'NOT'
            
        
    elif ch == '+': 
        _value = ch
        ch = mystr[_p]
        
        if ch =='+':            # '++'
            _value += ch
            _p += 1
            _syn = '++'
        else :                  # '+'
            _syn = 'PLUS'
        
    elif ch == '-': 
        _value = ch
        ch = mystr[_p]
        
        if ch =='-':            #'--'
            _value += ch
            _p += 1
            _syn = '--'
        else :                  # '-'
            _syn = 'MINUS'
            
    elif ch == '=':  
        _value = ch
        ch = mystr[_p]
        
        if ch =='=':            # '=='
            _value += ch
            _p += 1
            _syn = '=='
        else :                  # '='
            _syn = 'ASSIGNOP'
    
    elif ch == '&':
        _value = ch 
        ch = mystr[_p]
        
        if ch == '&':           # '&&'
            _value += ch
            _p += 1
            _syn = 'AND'
        else:                   # '&'
            _syn = '&'
            
    elif ch == '|':
        _value = ch
        ch = mystr[_p]
        
        if ch == '|':           # '||'       
            _value += ch
            _p += 1
            _syn = 'OR'
        else:                   # '|'
            _syn = '|'
    
    elif ch == '*':             # '*'
        _value = ch
        _syn = 'STAR'
        
    elif ch == '/':             # '/'
        _value = ch
        _syn = 'DIV'
        
    elif ch ==';':              # ';'
        _value = ch
        _syn = 'SEMI'
        
    elif ch == '(':             #  '('
        _value = ch
        _syn = 'LP'
        
    elif ch == ')':             # ')'
        _value = ch
        _syn = 'RP'
        
    elif ch == '{':             # '{'
        _value = ch
        _syn = 'LC'
        
    elif ch == '}':             # '}'    
        _value = ch
        _syn = 'RC'       
        
    elif ch == '[':             # '['    
        _value = ch
        _syn = 'LB'   
        
    elif ch == ']':             # ']'    
        _value = ch
        _syn = 'RB'  
        
    elif ch == ',':             # ','    
        _value = ch
        _syn = 'COMMA' 

    elif ch == '\n':
        _syn = 'error1'

if __name__ == '__main__': 
    getCode()
    clearComment()
    symbolTableFile = open(r'/home/jakevin/symbol_table.txt','w')
    tokenFile = open(r'/home/jakevin/token.txt','w')
    while _p != len(_content):
        getToken(_content)
        if _syn == 'error1':
            _line += 1 
        elif _syn == 'error2':
            print('string ' + _value + ' 不封闭! Error in line ' + str(_line))
        elif _syn == 'error3':
            print('number ' + _value + ' 错误，不能以0开头! Error in line ' + str(_line))
        elif _syn == 'error4':
            print('char ' + _value + ' 不封闭! Error in line ' + str(_line))
        elif _syn == 'error5':
            print('number ' + _value + ' 不合法! Error in line ' + str(_line))
        elif _syn == 'error6':
            print('identifier' + _value + ' 不能包含非法字符!Error in line ' + str(_line))
        elif _syn == 'error7':
            print('number ' + _value + ' 不合法,包含字母! Error in line ' + str(_line))
        else:
            #print((_syn,_value))
            tokenFile.write(str(_syn)+' , '+_value+'\n')
        
    tokenFile.close()
    symbolTableFile.write('入口地址\t变量名\n')
    i = 0
    for symbolItem in _symbol:
        symbolTableFile.write(str(i)+'\t\t\t'+symbolItem+'\n')
        i += 1
    symbolTableFile.close()       