import lexer
'''
class AST(object):
    def __init__(self, item):
        self.key = item
        self.lChild = None
        self.rChild = None
'''
p = 0
m = 0
value = ''
token = ''
syn = ''
ch = ''
content = ''
line = 0
state = ''



def Program():
    print("Program")
    ExtDefList()


def ExtDefList():
    print("ExtDefList")
    global syn, value, p, lists
    num = 0
    while ExtDef():
        num += 1
    if num >= 1:
        return True
    else:
        return False

def ExtDef():
    global syn, value, p
    if Specifier():
        if FunDec():
            if CompSt():
                return True
            return False
        elif ExtDefList():
            if SEMI():
                return True
        else:
            if SEMI():
                return True
    else:
        return False

def ExtDecList():
    global syn, value, p
    if VarDec():
        if COMMA():
            if ExtDecList():
                return True
            return False
        return True
    return False


def Specifier():
    global syn, value, p
    if TYPE():
        return True
    elif StructSpecifier():
        return True
    else:
        return False

def StructSpecifier():
    global syn, value, p
    if STRUCT():
        if LC():
            if DefList():
                if RC():
                    return True
    return False

def VarDec():
    global syn, value, p
    if ID():
        return True
    else:
        return False

def FunDec():
    global syn, value, p
    if ID():
        if LP():
            if VarList():
                if RP():
                    return True
            else:
                if RP():
                    return True
    return False


def VarList():
    global syn, value, p
    if ParamDec():
        if COMMA():
            if VarDec():
                return True
        else:
            return True
    return False


def ParamDec():
    global syn, value, p
    if Specifier():
        if VarDec():
            return True
    return False

def CompSt():
    if LC():
        if DefList():
            if StmtList():
                if RC():
                    return True
    return False

def StmtList():
    global syn, value, p
    num = 0
    while Stmt():
        num += 1
    if num >= 1:
        return True
    else:
        return False


def Stmt():
    global syn, value, p
    if Exp():
        if SEMI():
            return True
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
                    return True
    elif WHILE():
        if LP():
            if Exp():
                if RP():
                    if Stmt():
                        return True
    else:
        return False

def DefList():
    global syn, value, p
    num = 0
    while Def():
        num += 1
    if num >= 1:
        return True
    else:
        return False

def Def():
    global syn, value, p
    if Specifier():
        if DecList():
            if SEMI():
                return True
    else:
        return False

def DecList():
    global syn, value, p
    if Dec():
        if COMMA():
            if DecList():
                if SEMI():
                    return True
                return False
        return True
    return False

def Dec():
    global syn, value, p
    if VarDec():
        if ASSIGNOP():
            if Exp():
                return True
            return False
        return True
    return False

def Exp():
    global syn, value, p
    if LP():
        if Exp():
            if RP():
                if Exp1():
                    return True
    elif MINUS():
        if Exp():
            if Exp1():
                return True
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
    global syn, value, p
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
    global syn, value, p
    if Exp():
        if COMMA():
            if Args():
                return True
            return False
        return True
    return False

def COMMA():
    global syn, value, p
    if syn == 'COMMA':
        print('COMMA')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True


def ASSIGNOP():
    global syn, value, p
    if syn == 'ASSIGNOP':
        print('ASSIGNOP')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True


def RELOP():
    global syn, value, p
    if syn == 'RELOP':
        print('DIV')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True


def PLUS():
    global syn, value, p
    if syn == 'PLUS':
        print('PLUS')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True


def MINUS():
    global syn, value, p
    if syn == 'MINUS':
        print('MINUS')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True


def STAR():
    global syn, value, p
    if syn == 'STAR':
        print('STAR')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True



def DIV():
    global syn, value, p
    if syn == 'DIV':
        print('DIV')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True


def AND():
    global syn, value, p
    if syn == 'AND':
        print('AND')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True


def OR():
    global syn, value, p
    if syn == 'OR':
        print('OR')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True


def DOT():
    global syn, value, p
    if syn == 'DOT':
        print('DOT')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True

def NOT():
    global syn, value, p
    if syn == 'NOT':
        print('NOT')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True


def TYPE():
    print("TYPE")
    global syn, value, p
    if INT():
        return True
    elif FLOAT():
        return
    else:
        return False

def INT():
    global syn, value, p
    if syn == 'INT':
        print('INT')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True

def FLOAT():
    global syn, value, p
    if syn == 'FLOAT':
        print('FLOAT')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True


def LP():
    global syn, value, p
    if syn == 'LP':
        print('LP')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True

def RP():
    global syn, value, p
    if syn == 'RP':
        print('RP')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True

def LC():
    global syn, value, p
    if syn == 'LC':
        print('LC')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True

def RC():
    global syn, value, p
    if syn == 'RC':
        print('RC')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True

def STRUCT():
    global syn, value, p
    if syn == 'STRUCT':
        print('STRUCT')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True

def RETURN():
    global syn, value, p
    if syn == 'RETURN':
        print('RETURN')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True

def IF():
    global syn, value, p
    if syn == 'IF':
        print('IF')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True

def ELSE():
    global syn, value, p
    if syn == 'ELSE':
        print('ELSE')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True

def WHILE():
    global syn, value, p
    if syn == 'WHILE':
        print('WHILE')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True


def ID():
    global syn, value, p
    if syn == 'ID':
        print('ID')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True


def SEMI():
    global syn, value, p
    if syn == 'SEMI':
        print('SEMI')
        p, syn, value = lexer.get_token(content, p, syn, value)
        return True  # SEMI匹配后跳


if __name__ == '__main__':
    content = lexer.get_code(content)
    content = lexer.clear_comment(content)
    symbolTableFile = open(r'/home/jakevin/symbol_table.txt', 'w')
    tokenFile = open(r'/home/jakevin/token.txt', 'w')
    p, syn, value = lexer.get_token(content, p, syn, value)
    Program()
    tokenFile.close()

