import ast

class CostFunction:
    def __init__(self, formula):
        self.formula = formula
        self.astree = ast.parse(formula)
    
    # AST calculating and AST verify will be global
    # def evaluate(self, parameter_list):
    #     #TBD
    #     return 0