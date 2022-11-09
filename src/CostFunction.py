import ast

class CostFunction:
    def __init__(self, formula):
        self.formula = formula
        self.astree = ast.parse(cost_function.formula)
    
    def evaluate(self, parameter_list):
        #TBD
        return 0