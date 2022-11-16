import ast
import asteval

class EvalUtils:
    def __init__(self, formulas, iterating_parameter, parameter_list):
        self.formulas = formulas
        self.parameter_list = parameter_list
        self.iterating_parameter = iterating_parameter
        self.defined_vals = dict()
        self.construct_parameter_space(iterating_parameter, parameter_list)
    
    def construct_parameter_space(self, iterating_parameter, parameter_list):
        # add cost values for all parameters in the parameter space
        self.parameter_list = parameter_list
        for i in parameter_list:
            if(i.type != 'composite' and i.type != 'bool' and i.type != 'float'):
                self.defined_vals[i.name] = int(i.temporary_val)
            elif(i.type == 'float'):
                self.defined_vals[i.name] =  float(i.temporary_val)
            elif(i.type =='bool'):
                if(i.temporary_val) :
                    self.defined_vals[i.name] =  int(i.true_weight)
                else :
                    self.defined_vals[i.name] =  int(i.false_weight)
            else:
                for j in i.temporary_val:
                    for k in j:
                        if(k.type != 'composite' and k.type != 'bool'  and k.type != 'float'):
                            self.defined_vals[k.name] =  int(k.temporary_val)
                        elif(k.type == 'float'):
                            self.defined_vals[k.name] =  float(k.temporary_val)
                        elif(k.type =='bool'):
                            if(k.temporary_val) :
                                self.defined_vals[k.name] =  int(k.true_weight)
                            else :
                                self.defined_vals[k.name] =  int(k.false_weight)
        self.defined_vals[iterating_parameter.name] = iterating_parameter.temporary_val
        print(self.defined_vals)
        self.evaluator = asteval.Interpreter(usersyms=self.defined_vals)

class EvalCost(EvalUtils):
    def __init__(self, cost_formula, iterating_parameter, parameter_list):
        super().__init__(cost_formula, iterating_parameter, parameter_list)  

    def get_cost(self):
        self.tot_cost = self.evaluator(self.formulas)
        return self.tot_cost


class VerifyAssertions(EvalUtils):
    def __init__(self, assertions_formulas, iterating_parameter, parameter_list):
        super().__init__(assertions_formulas, iterating_parameter, parameter_list)

    def verify_assertions(self):
        all_asserts_valid = True
        for i in self.formulas.assertion_list:
            print(i)
            if self.evaluator(i):
                print("Assertion \t<<",i,">>\t holds in current state")
            else:
                print("Assertion \t<<",i,">>\t does NOT in current state")
                all_asserts_valid = False
        return False

class EvalStepFunction(EvalUtils):
    def __init__(self, step_function, iterating_parameter):
        super().__init__(step_function, iterating_parameter, [])

    def get_step(self):
        self.step = self.evaluator(self.formulas)
        return self.step