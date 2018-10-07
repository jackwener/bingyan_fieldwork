# compile error class
class CompileError(Exception):
    pass


class Check:
    # init
    def __init__(self):
        self.TABLE = {}
        self.error_message = ''
        self.label_no = 0

    # allocate label
    def get_label_no(self):
        self.label_no += 1
        return 'LABEL ' + str(self.label_no)

    # compare two types and raise error
    def compare_var_type(self, var_type_1, var_type_2):
        if var_type_1 == var_type_2:
            return var_type_1
        else:
            self.error_message = ''
            raise CompileError

    # build var table
    def build_table(self, x):
        

    def check_factor(self, factor):
        

    def check_factors(self, factor):
        

    def check_factor_c(self, fc):
        

    def check_term(self, term):
        

    def check_exp(self, x):
       

    def check_stm(self, x):
        

    def generate_factor(self, factor):
        

    def generate_factors(self, factors, factor):
       

    def generate_factor_c(self, fc):
       

    def generate_term(self, term, factor):
        

    def generate_exp(self, x):
        
    def generate_stm(self, x):
        

    def generate_func_blocks(self, x):
        

    def generate_func_block(self, x):
       

    def generate_else_block(self, x):
        

    def generate_logical(self, x):
        

    def generate_if(self, x):
        

    # dfs the ast tree
    def dfs(self, tree, func):
        func(tree)
        for i in range(1, len(tree)):
            v = tree[i]
            if type(v) == list:
                self.dfs(v, func)

    

if __name__ == '__main__':
    