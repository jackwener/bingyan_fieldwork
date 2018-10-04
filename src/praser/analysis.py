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

list_value = []
list_syn = []
list_line = []
m = 0

def Program():
    ExtDefList()


def ExtDefList():
    global list_line, list_syn, list_value, m
    m_tmp = m
    num = 0
    while ExtDef():
        num += 1
    if num >= 1:
        return True
    else:
        return False

def ExtDef():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if Specifier():
        if FunDec():
            if CompSt():
                return True
            return False
        elif ExtDecList():
            if SEMI():
                return True
            else :
                return False
        else:
            if SEMI():
                return True
    else:
        return False

def ExtDecList():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if VarDec():
        if COMMA():
            if ExtDecList():
                return True
            m = m_tmp
            return False
        return True
    m = m_tmp
    return False


def Specifier():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if TYPE():
        return True
    elif StructSpecifier():
        return True
    else:
        m = m_tmp
        return False

def StructSpecifier():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if STRUCT():
        if LC():
            if DefList():
                if RC():
                    return True
                else:
                    m = m_tmp
                    return False
            else:
                m = m_tmp
                return False
        else:
            m = m_tmp
            return False
    m = m_tmp
    return False

def VarDec():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if ID():
        return True
    else:
        return False

def FunDec():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if ID():
        if LP():
            if VarList():
                if RP():
                    return True
            else:
                if RP():
                    return True
        m = m_tmp
    m = m_tmp
    return False


def VarList():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if ParamDec():
        if COMMA():
            if VarDec():
                return True
        else:
            return True
    return False


def ParamDec():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if Specifier():
        if VarDec():
            return True
    return False

def CompSt():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if LC():
        if DefList():
            if StmtList():
                if RC():
                    return True
                else:
                    m = m_tmp
            else:
                m = m_tmp
                return False
        else:
            m = m_tmp
            return False
    else:
        m = m_tmp
        return False

def StmtList():
    global list_line, list_syn, list_value, m
    m_tmp = m
    num = 0
    while Stmt():
        num += 1
    return True


def Stmt():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if Exp():
        if SEMI():
            return True
        else:
            m = m_tmp
            return False
    elif CompSt():
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
                                m = m_tmp
                                return False
                        else:
                            m = m_tmp
                            return False
                    return True
                else:
                    m = m_tmp
                    return False
            else:
                m = m_tmp
                return False
        else:
            m = m_tmp
            return False
    elif WHILE():
        if LP():
            if Exp():
                if RP():
                    if Stmt():
                        return True
                    else:
                        m = m_tmp
                        return False
                else:
                    m = m_tmp
                    return False
            else:
                m = m_tmp
                return False
        else:
            m = m_tmp
            return False
    else:
        m = m_tmp
        return False

def DefList():
    global list_line, list_syn, list_value, m
    m_tmp = m
    num = 0
    while Def():
        num += 1
    return True

def Def():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if Specifier():
        if DecList():
            if SEMI():
                return True
            else:
                m = m_tmp
                return False
        else:
            m = m_tmp
            return False
    else:
        return False

def DecList():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if Dec():
        if COMMA():
            if DecList():
                return True
        return True
    return False

def Dec():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if VarDec():
        if ASSIGNOP():
            if Exp():
                return True
            return False
        return True
    return False

def Exp():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if LP():
        if Exp():
            if RP():
                if Exp1():
                    return True
                else:
                    m = m_tmp
                    return False
            else:
                m = m_tmp
        else:
            m = m_tmp
    elif MINUS():
        if Exp():
            if Exp1():
                return True
            else:
                m = m_tmp
        else:
            m = m_tmp
    elif NOT():
        if Exp():
            if Exp1():
                return True
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
    elif FLOAT():
        if Exp1():
            return True

def Exp1():
    global list_line, list_syn, list_value, m
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
    m_tmp = m
    if Exp():
        if COMMA():
            if Args():
                return True
            return False
        return True
    return False

def TYPE():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if INT():
        return True
    elif FLOAT():
        return True
    else:
        m = m_tmp
        return False


def COMMA():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'COMMA':
        print('COMMA')
        m += 1
        return True


def ASSIGNOP():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'ASSIGNOP':
        print('ASSIGNOP')
        m += 1
        return True


def RELOP():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'RELOP':
        print('RELOP')
        m += 1
        return True


def PLUS():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'PLUS':
        print('PLUS')
        m += 1
        return True


def MINUS():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'MINUS':
        print('MINUS')
        m += 1
        return True


def STAR():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'STAR':
        print('STAR')
        m += 1
        return True



def DIV():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'DIV':
        print('DIV')
        m += 1
        return True


def AND():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'AND':
        print('AND')
        m += 1
        return True


def OR():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'OR':
        print('OR')
        m += 1
        return True


def DOT():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'DOT':
        print('DOT')
        m += 1
        return True

def NOT():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'NOT':
        print('NOT')
        m += 1
        return True

def INT():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'INT':
        print('INT')
        m += 1
        return True

def FLOAT():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'FLOAT':
        print('FLOAT')
        m += 1
        return True


def LP():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'LP':
        print('LP')
        m += 1
        return True

def RP():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'RP':
        print('RP')
        m += 1
        return True

def LC():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'LC':
        print('LC')
        m += 1
        return True

def RC():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'RC':
        print('RC')
        m += 1
        return True

def STRUCT():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'STRUCT':
        print('STRUCT')
        m += 1
        return True

def RETURN():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'RETURN':
        print('RETURN')
        m += 1
        return True

def IF():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'IF':
        print('IF')
        m += 1
        return True

def ELSE():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'ELSE':
        print('ELSE')
        m += 1
        return True

def WHILE():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'WHILE':
        print('WHILE')
        m += 1
        return True


def ID():
    global list_line, list_syn, list_value, m
    m_tmp = m
    if list_syn[m] == 'ID':
        print('ID')
        m += 1
        return True


def SEMI():
    global list_line, list_syn, list_value, m
    if list_syn[m] == 'SEMI':
        print('SEMI')
        m += 1
        return True  # SEMI匹配后跳


if __name__ == '__main__':
    content = lexer.get_code(content)
    content = lexer.clear_comment(content)
    while syn != "#":
        p, syn, value, line = lexer.get_token(content, p, line)
        list_line.append(line)
        list_syn.append(syn)
        list_value.append(value)
    Program()
