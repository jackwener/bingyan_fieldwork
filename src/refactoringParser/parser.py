import lexer

TOKEN_STYLE = ['KEY_WORD', 'IDENTIFIER', 'DIGIT_CONSTANT',
               'OPERATOR', 'SEPARATOR', 'STRING_CONSTANT', 'CHAR_CONSTANT']

DETAIL_TOKEN_STYLE = {
    'include': 'INCLUDE',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'double': 'DOUBLE',
    'for': 'FOR',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'return': 'RETURN',
    '=': 'ASSIGN',
    '&': 'ADDRESS',
    "void": "VOID",
    '<': 'LT',
    '>': 'GT',
    '++': 'SELF_PLUS',
    '--': 'SELF_MINUS',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MUL',
    '/': 'DIV',
    '>=': 'GET',
    '<=': 'LET',
    '(': 'LL_BRACKET',
    ')': 'RL_BRACKET',
    '{': 'LB_BRACKET',
    '}': 'RB_BRACKET',
    '[': 'LM_BRACKET',
    ']': 'RM_BRACKET',
    ',': 'COMMA',
    '\"': 'DOUBLE_QUOTE',
    '\'': 'SINGLE_QUOTE',
    ';': 'SEMICOLON',
    '#': 'SHARP'}
# key word
keywords = [['int', 'float', 'double', 'char', 'void'],
            ['if', 'for', 'while', 'do', 'else'],
            ['include', 'return']]
# operator
operators = ['=', '&', '<', '>', '++', '--',
             '+', '-', '*', '/', '>=', '<=', '!=']
# separator
delimiters = ['(', ')', '{', '}', '[', ']', ',', '\"', ';', '\'']

p = 0
value = ''
token = ''
syn = ''
content = ''
line = 0

tokens = []

symbols = []

scope_list = []  # store scope of current


# symbol table node
class Symbol(object):
    def __init__(self,id,type,scope):
        self.id = id
        self.type = type
        self.scope = scope


class Token(object):
    def __init__(self,type,value):
        self.type = type
        self.value = value


class SyntaxTreeNode(object):
    """
    语法树节点
    """
    def __init__(self, value=None, _type=None, extra_info=None):
        # 节点的值，为文法中的终结符或者非终结符
        self.value = value
        # 记录某些token的类型
        self.type = _type
        # 语义分析中记录关于token的其他一些信息，比如关键字是变量，该变量类型为int
        self.extra_info = extra_info
        self.father = None
        self.left = None
        self.right = None
        self.first_son = None


    def set_value(self, value):
        self.value = value


    def set_type(self, _type):
        self.type = _type


    def set_extra_info(self, extra_info):
        self.extra_info = extra_info


class SyntaxTree(object):

    def __init__(self):
        # root
        self.root = None
        # the current node when travelling
        self.current = None

    # 添加一个子节点，必须确定father在该树中
    def add_child_node(self, new_node, father=None):
        if not father:
            father = self.current
        new_node.father = father
        # 如果father节点没有儿子，则将其赋值为其第一个儿子
        if not father.first_son:
            father.first_son = new_node
        else:
            current_node = father.first_son
            while current_node.right:
                current_node = current_node.right
            current_node.right = new_node
            new_node.left = current_node
        self.current = new_node

    # 交换相邻的两棵兄弟子树
    def switch(self, left, right):
        left_left = left.left
        right_right = right.right
        left.left = right
        left.right = right_right
        right.left = left_left
        right.right = left
        if left_left:
            left_left.right = right
        if right_right:
            right_right.left = left


class Parser_(object):

    def __init__(self,tokens):
        # tokens
        self.tokens = tokens
        self.index = 0
        # AST
        self.tree = SyntaxTree()

    # {}
    def _block(self, father_tree):
        self.index += 1
        sentence_tree = SyntaxTree()
        sentence_tree.current = sentence_tree.root = SyntaxTreeNode('Sentence')
        father_tree.add_child_node(sentence_tree.root, father_tree.root)
        while True:
            sentence_pattern = self._judge_sentence_pattern()
            if sentence_pattern == 'STATEMENT':
                self._statement(sentence_tree.root)
            elif sentence_pattern == 'ASSIGNMENT':
                self._assignment(sentence_tree.root)
            elif sentence_pattern == 'FUNCTION_CALL':
                self._function_call(sentence_tree.root)
            elif sentence_pattern == 'FUNCTION_STATEMENT':
                self._function_statement(sentence_tree.root)
            elif sentence_pattern == 'CONTROL':
                self._control(sentence_tree.root)
            elif sentence_pattern == 'RETURN':
                self._return(sentence_tree.root)
            # }
            elif sentence_pattern == 'RB_BRACKET':
                break
            else:
                print('block error!')
                exit()


    def _function_statement(self, father=None):
        if not father:
            father = self.tree.root
        func_statement_tree = SyntaxTree()
        func_statement_tree.current = func_statement_tree.root = SyntaxTreeNode(
            'FunctionStatement')
        self.tree.add_child_node(func_statement_tree.root, father)
        flag = True
        while flag and self.index < len(self.tokens):
            # return
            if self.tokens[self.index].value in keywords[0]:
                return_type = SyntaxTreeNode('Type')
                func_statement_tree.add_child_node(return_type)
                func_statement_tree.add_child_node(
                    SyntaxTreeNode(self.tokens[self.index].value, 'FIELD_TYPE',
                                   {'type': self.tokens[self.index].value}))
                self.index += 1
            # func name
            elif self.tokens[self.index].type == 'IDENTIFIER':
                func_name = SyntaxTreeNode('FunctionName')
                func_statement_tree.add_child_node(
                    func_name, func_statement_tree.root)
                # extra_info
                func_statement_tree.add_child_node(
                    SyntaxTreeNode(self.tokens[self.index].value, 'IDENTIFIER', {'type': 'FUNCTION_NAME'}))
                self.index += 1
            # argsList
            elif self.tokens[self.index].type == 'LL_BRACKET':
                params_list = SyntaxTreeNode('StateParameterList')
                func_statement_tree.add_child_node(
                    params_list, func_statement_tree.root)
                self.index += 1
                while self.tokens[self.index].type != 'RL_BRACKET':
                    if self.tokens[self.index].value in keywords[0]:
                        param = SyntaxTreeNode('Parameter')
                        func_statement_tree.add_child_node(param, params_list)
                        # extra_info
                        func_statement_tree.add_child_node(
                            SyntaxTreeNode(self.tokens[self.index].value, 'FIELD_TYPE',
                                           {'type': self.tokens[self.index].value}), param)
                        if self.tokens[self.index + 1].type == 'IDENTIFIER':
                            # extra_info
                            func_statement_tree.add_child_node(
                                SyntaxTreeNode(self.tokens[self.index + 1].value, 'IDENTIFIER',
                                               {'type': 'VARIABLE', 'variable_type': self.tokens[self.index].value}),
                                param
                            )
                        else:
                            print ('函数定义参数错误！')
                            exit()
                        self.index += 1
                    self.index += 1
                self.index += 1
            # {
            elif self.tokens[self.index].type == 'LB_BRACKET':
                self._block(func_statement_tree)
                flag = False

    def _statement(self, father=None):
        if not father:
            father = self.tree.root
        statement_tree = SyntaxTree()
        statement_tree.current = statement_tree.root = SyntaxTreeNode(
            'Statement')
        self.tree.add_child_node(statement_tree.root, father)
        tmp_variable_type = None
        while self.tokens[self.index].type != 'SEMICOLON':
            if self.tokens[self.index].value in keywords[0]:
                tmp_variable_type = self.tokens[self.index].value
                variable_type = SyntaxTreeNode('Type')
                statement_tree.add_child_node(variable_type)
                # extra_info
                statement_tree.add_child_node(
                    SyntaxTreeNode(self.tokens[self.index].value, 'FIELD_TYPE',
                                   {'type': self.tokens[self.index].value}))
            elif self.tokens[self.index].type == 'IDENTIFIER':
                # extra_info
                statement_tree.add_child_node(SyntaxTreeNode(self.tokens[self.index].value, 'IDENTIFIER', {
                    'type': 'VARIABLE', 'variable_type': tmp_variable_type}),
                                              statement_tree.root)
            elif self.tokens[self.index].type == 'DIGIT_CONSTANT':
                statement_tree.add_child_node(
                    SyntaxTreeNode(self.tokens[self.index].value, 'DIGIT_CONSTANT'), statement_tree.root)
                statement_tree.current.left.set_extra_info(
                    {'type': 'LIST', 'list_type': tmp_variable_type})
            elif self.tokens[self.index].type == 'LB_BRACKET':
                self.index += 1
                constant_list = SyntaxTreeNode('ConstantList')
                statement_tree.add_child_node(
                    constant_list, statement_tree.root)
                while self.tokens[self.index].type != 'RB_BRACKET':
                    if self.tokens[self.index].type == 'DIGIT_CONSTANT':
                        statement_tree.add_child_node(
                            SyntaxTreeNode(self.tokens[self.index].value, 'DIGIT_CONSTANT'), constant_list)
                    self.index += 1
            elif self.tokens[self.index].type == 'COMMA':
                while self.tokens[self.index].type != 'SEMICOLON':
                    if self.tokens[self.index].type == 'IDENTIFIER':
                        tree = SyntaxTree()
                        tree.current = tree.root = SyntaxTreeNode('Statement')
                        self.tree.add_child_node(tree.root, father)
                        # tyoe
                        variable_type = SyntaxTreeNode('Type')
                        tree.add_child_node(variable_type)
                        # extra_info
                        # type
                        tree.add_child_node(
                            SyntaxTreeNode(tmp_variable_type, 'FIELD_TYPE', {'type': tmp_variable_type}))
                        # var name
                        tree.add_child_node(SyntaxTreeNode(self.tokens[self.index].value, 'IDENTIFIER', {
                            'type': 'VARIABLE', 'variable_type': tmp_variable_type}), tree.root)
                    self.index += 1
                break
            self.index += 1
        self.index += 1

    def _assignment(self, father=None):
        if not father:
            father = self.tree.root
        assign_tree = SyntaxTree()
        assign_tree.current = assign_tree.root = SyntaxTreeNode('Assignment')
        self.tree.add_child_node(assign_tree.root, father)
        while self.tokens[self.index].type != 'SEMICOLON':
            if self.tokens[self.index].type == 'IDENTIFIER':
                assign_tree.add_child_node(
                    SyntaxTreeNode(self.tokens[self.index].value, 'IDENTIFIER'))
                self.index += 1
            elif self.tokens[self.index].type == 'ASSIGN':
                self.index += 1
                self._expression(assign_tree.root)
        self.index += 1

    def _while(self, father=None):
        while_tree = SyntaxTree()
        while_tree.current = while_tree.root = SyntaxTreeNode(
            'Control', 'WhileControl')
        self.tree.add_child_node(while_tree.root, father)

        token_type = self.tokens[self.index].type
        if token_type == 'WHILE':
            self.index += 1
        if self.tokens[self.index].type == 'LL_BRACKET':
            self.index += 1
            tmp_index = self.index
            while self.tokens[tmp_index].type != 'RL_BRACKET':
                tmp_index += 1
            self._expression(while_tree.root, tmp_index)
            # while content
            self.index += 1
            if self.tokens[self.index].type == 'LB_BRACKET':
                self._block(while_tree)

    # for
    def _for(self, father=None):
        for_tree = SyntaxTree()
        for_tree.current = for_tree.root = SyntaxTreeNode(
            'Control', 'ForControl')
        self.tree.add_child_node(for_tree.root, father)
        while True:
            token_type = self.tokens[self.index].type
            if token_type == 'FOR':
                self.index += 1
            elif token_type == 'LL_BRACKET':
                self.index += 1
                # )
                tmp_index = self.index
                while self.tokens[tmp_index].type != 'RL_BRACKET':
                    tmp_index += 1
                self._assignment(for_tree.root)
                self._expression(for_tree.root)
                self.index += 1
                self._expression(for_tree.root, tmp_index)
                self.index += 1
            # {
            elif token_type == 'LB_BRACKET':
                self._block(for_tree)
                break
        # 交换for语句下第三个子节点和第四个子节点
        current_node = for_tree.root.first_son.right.right
        next_node = current_node.right
        for_tree.switch(current_node, next_node)

    # if
    def _if_else(self, father=None):
        if_else_tree = SyntaxTree()
        if_else_tree.current = if_else_tree.root = SyntaxTreeNode(
            'Control', 'IfElseControl')
        self.tree.add_child_node(if_else_tree.root, father)

        if_tree = SyntaxTree()
        if_tree.current = if_tree.root = SyntaxTreeNode('IfControl')
        if_else_tree.add_child_node(if_tree.root)

        # if
        if self.tokens[self.index].type == 'IF':
            self.index += 1
            # (
            if self.tokens[self.index].type == 'LL_BRACKET':
                self.index += 1
                # )
                tmp_index = self.index
                while self.tokens[tmp_index].type != 'RL_BRACKET':
                    tmp_index += 1
                self._expression(if_tree.root, tmp_index)
                self.index += 1
            else:
                print ('error: lack of left bracket!')
                exit()

            # {
            if self.tokens[self.index].type == 'LB_BRACKET':
                self._block(if_tree)

        # else
        if self.tokens[self.index].type == 'ELSE':
            self.index += 1
            else_tree = SyntaxTree()
            else_tree.current = else_tree.root = SyntaxTreeNode('ElseControl')
            if_else_tree.add_child_node(else_tree.root, if_else_tree.root)
            # }
            if self.tokens[self.index].type == 'LB_BRACKET':
                self._block(else_tree)

    def _control(self, father=None):
        token_type = self.tokens[self.index].type
        if token_type == 'WHILE' or token_type == 'DO':
            self._while(father)
        elif token_type == 'IF':
            self._if_else(father)
        elif token_type == 'FOR':
            self._for(father)
        else:
            print ('error: control style not supported!')
            exit()

    def _expression(self, father=None, index=None):
        if not father:
            father = self.tree.root
        # Operator precedence
        operator_priority = {'>': 0, '<': 0, '>=': 0, '<=': 0, '(': -1,
                             '+': 1, '-': 1, '*': 2, '/': 2, '++': 3, '--': 3, '!': 3}
        # Operator stack
        operator_stack = []
        # 转换成的逆波兰表达式结果
        reverse_polish_expression = []
        # 中缀表达式转为后缀表达式，即逆波兰表达式
        while self.tokens[self.index].type != 'SEMICOLON':
            if index and self.index >= index:
                break
            if self.tokens[self.index].type == 'DIGIT_CONSTANT':
                tree = SyntaxTree()
                tree.current = tree.root = SyntaxTreeNode(
                    'Expression', 'Constant')
                tree.add_child_node(
                    SyntaxTreeNode(self.tokens[self.index].value, '_Constant'))
                reverse_polish_expression.append(tree)
            elif self.tokens[self.index].type == 'IDENTIFIER':
                # var
                if self.tokens[self.index + 1].value in operators or \
                                self.tokens[self.index + 1].type == 'SEMICOLON' or \
                                self.tokens[self.index + 1].type == 'RL_BRACKET':
                # if self.tokens[self.index + 1].value in operators or self.tokens[self.index + 1].type == 'SEMICOLON':
                    tree = SyntaxTree()
                    tree.current = tree.root = SyntaxTreeNode(
                        'Expression', 'Variable')
                    tree.add_child_node(
                        SyntaxTreeNode(self.tokens[self.index].value, '_Variable'))
                    reverse_polish_expression.append(tree)
                elif self.tokens[self.index + 1].type == 'LM_BRACKET':
                    tree = SyntaxTree()
                    tree.current = tree.root = SyntaxTreeNode(
                        'Expression', 'ArrayItem')
                    # Array name
                    tree.add_child_node(
                        SyntaxTreeNode(self.tokens[self.index].value, '_ArrayName'))
                    self.index += 2
                    if self.tokens[self.index].type != 'DIGIT_CONSTANT' and \
                                    self.tokens[self.index].type != 'IDENTIFIER':
                        print ('error: 数组下表必须为常量或标识符')
                        print (self.tokens[self.index].type)
                        exit()
                    else:
                        # Array subscript
                        tree.add_child_node(
                            SyntaxTreeNode(self.tokens[self.index].value, '_ArrayIndex'), tree.root)
                        reverse_polish_expression.append(tree)
            elif self.tokens[self.index].value in operators or self.tokens[self.index].type == 'LL_BRACKET' \
                    or self.tokens[self.index].type == 'RL_BRACKET':
                tree = SyntaxTree()
                tree.current = tree.root = SyntaxTreeNode(
                    'Operator', 'Operator')
                tree.add_child_node(
                    SyntaxTreeNode(self.tokens[self.index].value, '_Operator'))
                # ( -> Push stack
                if self.tokens[self.index].type == 'LL_BRACKET':
                    operator_stack.append(tree)
                # ) - Pop stack
                elif self.tokens[self.index].type == 'RL_BRACKET':
                    while operator_stack and operator_stack[-1].current.value != '(':
                        reverse_polish_expression.append(operator_stack.pop())
                    # pop (
                    if operator_stack:
                        operator_stack.pop()
                #  operators
                else:
                    while operator_stack and operator_priority[tree.current.value] <= \
                            operator_priority[operator_stack[-1].current.value]:
                        reverse_polish_expression.append(operator_stack.pop())
                    operator_stack.append(tree)
            self.index += 1
        while operator_stack:
            reverse_polish_expression.append(operator_stack.pop())
        for item in reverse_polish_expression:
            print(item.current.value,)

        # Operand stack
        operand_stack = []
        child_operators = [['!', '++', '--'], [
            '+', '-', '*', '/', '>', '<', '>=', '<=']]
        for item in reverse_polish_expression:
            if item.root.type != 'Operator':
                operand_stack.append(item)
            else:
                # Monocular operator
                if item.current.value in child_operators[0]:
                    a = operand_stack.pop()
                    new_tree = SyntaxTree()
                    new_tree.current = new_tree.root = SyntaxTreeNode(
                        'Expression', 'SingleOperand')
                    # Add operator
                    new_tree.add_child_node(item.root)
                    # Add operand
                    new_tree.add_child_node(a.root, new_tree.root)
                    operand_stack.append(new_tree)
                # Binocular operator
                elif item.current.value in child_operators[1]:
                    b = operand_stack.pop()
                    a = operand_stack.pop()
                    new_tree = SyntaxTree()
                    new_tree.current = new_tree.root = SyntaxTreeNode(
                        'Expression', 'DoubleOperand')
                    # first operand
                    new_tree.add_child_node(a.root)
                    # operator
                    new_tree.add_child_node(item.root, new_tree.root)
                    # second operand
                    new_tree.add_child_node(b.root, new_tree.root)
                    operand_stack.append(new_tree)
                else:
                    print('operator %s not supported!' % item.current.value)
                    exit()
        self.tree.add_child_node(operand_stack[0].root, father)

    # Function Call
    def _function_call(self, father=None):
        if not father:
            father = self.tree.root
        func_call_tree = SyntaxTree()
        func_call_tree.current = func_call_tree.root = SyntaxTreeNode(
            'FunctionCall')
        self.tree.add_child_node(func_call_tree.root, father)

        while self.tokens[self.index].type != 'SEMICOLON':
            # Func name
            if self.tokens[self.index].type == 'IDENTIFIER':
                func_call_tree.add_child_node(
                    SyntaxTreeNode(self.tokens[self.index].value, 'FUNCTION_NAME'))
            # (
            elif self.tokens[self.index].type == 'LL_BRACKET':
                self.index += 1
                params_list = SyntaxTreeNode('CallParameterList')
                func_call_tree.add_child_node(params_list, func_call_tree.root)
                while self.tokens[self.index].type != 'RL_BRACKET':
                    if self.tokens[self.index].type == 'IDENTIFIER' or self.tokens[self.index].type == 'DIGIT_CONSTANT' \
                            or self.tokens[self.index].type == 'STRING_CONSTANT':
                        func_call_tree.add_child_node(
                            SyntaxTreeNode(self.tokens[self.index].value, self.tokens[self.index].type), params_list)
                    elif self.tokens[self.index].type == 'DOUBLE_QUOTE':
                        self.index += 1
                        func_call_tree.add_child_node(
                            SyntaxTreeNode(self.tokens[self.index].value, self.tokens[self.index].type), params_list)
                        self.index += 1
                    elif self.tokens[self.index].type == 'ADDRESS':
                        func_call_tree.add_child_node(
                            SyntaxTreeNode(self.tokens[self.index].value, 'ADDRESS'), params_list)
                    self.index += 1
            else:
                print('function call error!')
                exit()
            self.index += 1
        self.index += 1

    def _return(self, father=None):
        if not father:
            father = self.tree.root
        return_tree = SyntaxTree()
        return_tree.current = return_tree.root = SyntaxTreeNode('Return')
        self.tree.add_child_node(return_tree.root, father)
        while self.tokens[self.index].type != 'SEMICOLON':
            if self.tokens[self.index].type == 'RETURN':
                return_tree.add_child_node(
                    SyntaxTreeNode(self.tokens[self.index].value))
                self.index += 1
            else:
                self._expression(return_tree.root)
        self.index += 1

    def _judge_sentence_pattern(self):
        token_value = self.tokens[self.index].value
        token_type = self.tokens[self.index].type
        if token_value in keywords[1]:
            return 'CONTROL'
        # Declaration statement or function declaration statement
        elif token_value in keywords[0] and self.tokens[self.index + 1].type == 'IDENTIFIER':
            index_2_token_type = self.tokens[self.index + 2].type
            if index_2_token_type == 'LL_BRACKET':
                return 'FUNCTION_STATEMENT'
            elif index_2_token_type == 'SEMICOLON' or index_2_token_type == 'LM_BRACKET' \
                    or index_2_token_type == 'COMMA':
                return 'STATEMENT'
            else:
                return 'ERROR'
        # function call or assignment statement
        elif token_type == 'IDENTIFIER':
            index_1_token_type = self.tokens[self.index + 1].type
            if index_1_token_type == 'LL_BRACKET':
                return 'FUNCTION_CALL'
            elif index_1_token_type == 'ASSIGN':
                return 'ASSIGNMENT'
            else:
                return 'ERROR'
        # return
        elif token_type == 'RETURN':
            return 'RETURN'
        # } the end
        elif token_type == 'RB_BRACKET':
            self.index += 1
            return 'RB_BRACKET'
        else:
            return 'ERROR'


    def main(self):
        # Root node
        self.tree.current = self.tree.root = SyntaxTreeNode('Sentence')
        while self.index < len(self.tokens):
            sentence_pattern = self._judge_sentence_pattern()
            # Function declaration statement
            if sentence_pattern == 'FUNCTION_STATEMENT':
                self._function_statement()
                break
            # Statement statement
            elif sentence_pattern == 'STATEMENT':
                self._statement()
            # Function call
            elif sentence_pattern == 'FUNCTION_CALL':
                self._function_call()
            else:
                print('main error!')
                exit()

    # DFS traversing the syntax tree
    def dfs(self, node):
        if not node:
            return
        print('( self: %s %s, father: %s, left: %s, right: %s )' % (node.value, node.type,
                                                                    node.father.value if node.father else None,
                                                                    node.left.value if node.left else None,
                                                                    node.right.value if node.right else None))
        child = node.first_son
        while child:
            self.dfs(child)
            child = child.right


if __name__ == '__main__':
    content = lexer.get_code(content)
    content = lexer.clear_comment(content)
    lens = len(content)
    while p < lens:
        p, syn, value, line = lexer.get_token(content, p, line)
        if syn == 'error1':
            print('string ' + value + ' Not closed! Error in line ' + str(line))
        elif syn == 'error2':
            print('number ' + value + ' Cannot start with 0! Error in line ' + str(line))
        elif syn == 'error3':
            print('char ' + value + ' Not closed! Error in line ' + str(line))
        elif syn == 'error4':
            print('number ' + value + ' illegal! Error in line ' + str(line))
        elif syn == 'error5':
            print('identifier' + value + ' contain illegal characters!Error in line ' + str(line))
        elif syn == 'error6':
            print('number ' + value + ' Contains letters! Error in line ' + str(line))
        tokens.append(Token(type=syn,value=value))
    for tok in tokens:
        print(tok.type,tok.value)
    parser = Parser_(tokens=tokens)
    parser.main()
    parser.dfs(parser.tree.root)