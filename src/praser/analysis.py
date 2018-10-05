import lexer
'''
class AST(object):
    def __init__(self, item):
        self.key = item
        self.lChild = None
        self.rChild = None
'''
end = ('SEMI','ID','STRUCT','RETURN','IF','ELSE','WHILE',
'RC','LC','RP','LP','FLOAT','INT','NOT','DOT','OR','AND',
'DIV','STAR','MINUS','PLUS','RELOP','ASSIGNOP','COMMA')


p = 0
value = ''
token = ''
syn = ''
ch = ''
content = ''
line = 0
state = ''

list = []

list_value = []
list_syn = []
list_line = []
m = 0

def Program():
    global L
    if ExtDefList():
        print("success")


def ExtDefList():
    global list_line, list_syn, list_value
    n = 0
    list.append('ExtDefList')
    while ExtDef():
        n += 1
    return True

def ExtDef():
    global list_line, list_syn, list_value, m
    m_tmp = m
    n = 0
    if list_syn[m] == '#':
        return False
    elif Specifier():
        if FunDec():
            if CompSt():
                return True
            while list.pop() == 'ExtDef':
                n += 1
            return False
        elif ExtDecList():
            if SEMI():
                return True
            else :
                while list.pop() == 'ExtDef':
                    n += 1
                return False
        else:
            if SEMI():
                return True
    else:
        while list.pop() == 'ExtDef':
            n += 1
        return False

def ExtDecList():
    global list_line, list_syn, list_value, m,L
    n = 0
    list.append('ExtDecList')
    m_tmp = m
    if VarDec():
        if COMMA():
            if ExtDecList():
                return True
            while list.pop() == 'ExtDecList':
                n += 1
            m = m_tmp
            return False
        return True
    while list.pop() == 'ExtDecList':
        n += 1
    m = m_tmp
    return False


def Specifier():
    global list_line, list_syn, list_value, m
    list.append('Specifier')
    n = 0
    m_tmp = m
    if TYPE():
        return True
    elif StructSpecifier():
        return True
    else:
        while list.pop() == 'Specifier':
            n += 1
        m = m_tmp
        return False

def StructSpecifier():
    global list_line, list_syn, list_value, m
    list.append('StructSpecifier')
    n = 0
    m_tmp = m
    if STRUCT():
        if LC():
            if DefList():
                if RC():
                    return True
                else:
                    while list.pop() == 'StructSpecifier':
                        n += 1
                    m = m_tmp
                    return False
            else:
                while list.pop() == 'StructSpecifier':
                    n += 1
                m = m_tmp
                return False
        else:
            while list.pop() == 'StructSpecifier':
                n += 1
            m = m_tmp
            return False
    while list.pop() == 'StructSpecifier':
        n += 1
    m = m_tmp
    return False

def VarDec():
    list.append('VarDec')
    n = 0
    global list_line, list_syn, list_value, m
    m_tmp = m
    if ID():
        return True
    else:
        while list.pop() == 'VarDec':
            n += 1
        m = m_tmp
        return False

def FunDec():
    global list_line, list_syn, list_value, m
    list.append('FunDec')
    n = 0
    m_tmp = m
    if ID():
        if LP():
            if VarList():
                if RP():
                    return True
            else:
                if RP():
                    return True
        while list.pop() == 'FunDec':
            n += 1
        m = m_tmp
        return False
    while list.pop() == 'FunDec':
        n += 1
    m = m_tmp
    return False


def VarList():
    global list_line, list_syn, list_value, m
    list.append('VarList')
    n = 0
    m_tmp = m
    if ParamDec():
        if COMMA():
            if VarDec():
                return True
        else:
            return True
    while list.pop() == 'VarList':
        n += 1
    m = m_tmp
    return False


def ParamDec():
    global list_line, list_syn, list_value, m
    list.append('ParamDec')
    n = 0
    m_tmp = m
    if Specifier():
        if VarDec():
            return True
    while list.pop() == 'ParamDec':
        n += 1
    m = m_tmp
    return False

def CompSt():
    list.append('CompSt')
    n = 0
    global list_line, list_syn, list_value, m
    m_tmp = m
    if LC():
        if DefList():
            if StmtList():
                if RC():
                    return True
                else:
                    while list.pop() == 'CompSt':
                        n += 1
                    m = m_tmp
            else:
                while list.pop() == 'CompSt':
                    n += 1
                m = m_tmp
                return False
        else:
            while list.pop() == 'CompSt':
                n += 1
            m = m_tmp
            return False
    else:
        while list.pop() == 'CompSt':
            n += 1
        m = m_tmp
        return False

def StmtList():
    global list_line, list_syn, list_value, m
    list.append('StmtList')
    m_tmp = m
    num = 0
    while Stmt():
        num += 1
    return True


def Stmt():
    global list_line, list_syn, list_value, m
    list.append('Stmt')
    n = 0
    m_tmp = m
    if Exp():
        if SEMI():
            return True
        else:
            while list.pop() == 'Stmt':
                n += 1
            m = m_tmp
            return False
    elif CompSt():
        return True
    elif RETURN():
        if Exp():
            if SEMI():
                return True
    elif IF():
        if LP():
            if Exp():
                if RP():
                    if Stmt():
                        if ELSE():
                            if Stmt():
                                return True
                            else:
                                while list.pop() == 'Stmt':
                                    n += 1
                                m = m_tmp
                                return False
                        else:
                            return True
                    else:
                        while list.pop() == 'Stmt':
                            n += 1
                        m = m_tmp
                        return False
                else:
                    while list.pop() == 'Stmt':
                        n += 1
                    m = m_tmp
                    return False
            else:
                while list.pop() == 'Stmt':
                    n += 1
                m = m_tmp
                return False
        else:
            while list.pop() == 'Stmt':
                n += 1
            m = m_tmp
            return False
    elif WHILE():
        if LP():
            if Exp():
                if RP():
                    if Stmt():
                        return True
                    else:
                        while list.pop() == 'Stmt':
                            n += 1
                        m = m_tmp
                        return False
                else:
                    while list.pop() == 'Stmt':
                        n += 1
                    m = m_tmp
                    return False
            else:
                while list.pop() == 'Stmt':
                    n += 1
                m = m_tmp
                return False
        else:
            while list.pop() == 'Stmt':
                n += 1
            m = m_tmp
            return False
    else:
        while list.pop() == 'Stmt':
            n += 1
        m = m_tmp
        return False

def DefList():
    global list_line, list_syn, list_value, m
    list.append('DefList')
    m_tmp = m
    num = 0
    while Def():
        num += 1
    return True

def Def():
    global list_line, list_syn, list_value, m
    list.append('Def')
    n = 0
    m_tmp = m
    if Specifier():
        if DecList():
            if SEMI():
                return True
            else:
                while list.pop() == 'Def':
                    n += 1
                m = m_tmp
                return False
        else:
            while list.pop() == 'Def':
                n += 1
            m = m_tmp
            return False
    else:
        while list.pop() == 'Def':
            n += 1
        m = m_tmp
        return False

def DecList():
    global list_line, list_syn, list_value, m
    list.append('DecList')
    n = 0
    m_tmp = m
    if Dec():
        if COMMA():
            if DecList():
                return True
            while list.pop() == 'DecList':
                n += 1
            m = m_tmp
            return  False
        return True
    while list.pop() == 'DecList':
        n += 1
    m = m_tmp
    return False

def Dec():
    global list_line, list_syn, list_value, m
    list.append('Dec')
    n = 0
    m_tmp = m
    if VarDec():
        if ASSIGNOP():
            if Exp():
                return True
            while list.pop() == 'Dec':
                n += 1
            m = m_tmp
            return False
        return True
    while list.pop() == 'Dec':
        n += 1
    m = m_tmp
    return False

def Exp():
    global list_line, list_syn, list_value, m
    list.append('Exp')
    n = 0
    m_tmp = m
    if LP():
        if Exp():
            if RP():
                if Exp1():
                    return True
                else:
                    while list.pop() == 'Exp':
                        n += 1
                    m = m_tmp
                    return False
            else:
                while list.pop() == 'Exp':
                    n += 1
                m = m_tmp
        else:
            while list.pop() == 'Exp':
                n += 1
            m = m_tmp
    elif MINUS():
        if Exp():
            if Exp1():
                return True
            else:
                while list.pop() == 'Exp':
                    n += 1
                m = m_tmp
        else:
            while list.pop() == 'Exp':
                n += 1
            m = m_tmp
    elif NOT():
        if Exp():
            if Exp1():
                return True
        else:
            while list.pop() == 'Exp':
                n += 1
            m = m_tmp
    elif ID():
        if LP():
            if Args():
                if RP():
                    if Exp1():
                        return True
            elif RP():
                if Exp1():
                    return True
        elif Exp1():
            return True
    elif INT():
        if Exp1():
            return True
        else:
            while list.pop() == 'Exp':
                n += 1
            m = m_tmp
    elif FLOAT():
        if Exp1():
            return True
        else:
            while list.pop() == 'Exp':
                n += 1
            m = m_tmp
    else:
        while list.pop() == 'Exp':
            n += 1
        m = m_tmp

def Exp1():
    global list_line, list_syn, list_value, m
    list.append('Exp1')
    m_tmp = m
    if ASSIGNOP():
        if Exp():
            return True
    elif OR():
        if Exp():
            return True
    elif RELOP():
        if Exp():
            return True
    elif PLUS():
        if Exp():
            return True
    elif MINUS():
        if Exp():
            return True
    elif STAR():
        if Exp():
            return True
    elif DIV():
        if Exp():
            return True
    elif DOT():
        if ID():
            return True
    else:
        return True

def Args():
    global list_line, list_syn, list_value, m
    list.append('Args')
    n = 0
    m_tmp = m
    if Exp():
        if COMMA():
            if Args():
                return True
            while list.pop() == 'Args':
                n += 1
            m = m_tmp
            return False
        return True
    while list.pop() == 'Args':
        n += 1
    m = m_tmp
    return False

def TYPE():
    global list_line, list_syn, list_value, m
    list.append('TYPE')
    n = 0
    m_tmp = m
    if list_syn[m] == 'INT':
        m += 1
        list.append(':INT')
        return True
    elif list_syn[m] == 'FLOAT':
        list.append(':FLOAT')
        m += 1
        return True
    else:
        while list.pop() == 'TYPE':
            n += 1
        m = m_tmp
        return False


def COMMA():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'COMMA':
        list.append('COMMA')
        m += 1
        return True


def ASSIGNOP():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'ASSIGNOP':
        list.append('ASSIGNOP')
        m += 1
        return True


def RELOP():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'RELOP':
        list.append('RELOP')
        m += 1
        return True


def PLUS():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'PLUS':
        list.append('PLUS')
        m += 1
        return True


def MINUS():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'MINUS':
        list.append('MINUS')
        m += 1
        return True


def STAR():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'STAR':
        list.append('STAR')
        m += 1
        return True



def DIV():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'DIV':
        list.append('DIV')
        m += 1
        return True


def AND():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'AND':
        list.append('AND')
        m += 1
        return True


def OR():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'OR':
        list.append('OR')
        m += 1
        return True


def DOT():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'DOT':
        list.append('DOT')
        m += 1
        return True

def NOT():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'NOT':
        list.append('NOT')
        m += 1
        return True

def INT():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'INT':
        list.append('INT')
        m += 1
        return True

def FLOAT():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'FLOAT':
        list.append('FLOAT')
        m += 1
        return True


def LP():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'LP':
        list.append('LP')
        m += 1
        return True

def RP():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'RP':
        list.append('RP')
        m += 1
        return True

def LC():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'LC':
        list.append('LC')
        m += 1
        return True

def RC():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'RC':
        list.append('RC')
        m += 1
        return True

def STRUCT():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'STRUCT':
        list.append('STRUCT')
        m += 1
        return True

def RETURN():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'RETURN':
        list.append('RETURN')
        m += 1
        return True

def IF():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'IF':
        list.append('IF')
        m += 1
        return True

def ELSE():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'ELSE':
        list.append('ELSE')
        m += 1
        return True

def WHILE():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'WHILE':
        list.append('WHILE')
        m += 1
        return True


def ID():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'ID':
        list.append('ID')
        m += 1
        return True


def SEMI():
    global list_line, list_syn, list_value, m
    if list_syn[m] == 'SEMI':
        list.append('SEMI')
        m += 1
        return True


if __name__ == '__main__':
    content = lexer.get_code(content)
    content = lexer.clear_comment(content)
    while syn != "#":
        p, syn, value, line = lexer.get_token(content, p, line)
        if syn == 'error2':
            print('string ' + value + ' 不封闭! Error in line ' + str(line))
        elif syn == 'error3':
            print('number ' + value + ' 错误，不能以0开头! Error in line ' + str(line))
        elif syn == 'error4':
            print('char ' + value + ' 不封闭! Error in line ' + str(line))
        elif syn == 'error5':
            print('number ' + value + ' 不合法! Error in line ' + str(line))
        elif syn == 'error6':
            print('identifier' + value + ' 不能包含非法字符!Error in line ' + str(line))
        elif syn == 'error7':
            print('number ' + value + ' 不合法,包含字母! Error in line ' + str(line))
        list_line.append(line)
        list_syn.append(syn)
        list_value.append(value)
    Program()
    for item in list:
        print(item)
