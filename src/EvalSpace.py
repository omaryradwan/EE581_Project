import ast
import asteval

class EvalCost:
    def __init__(self, cost_formula):
        self.cost_formula = cost_formula
        self.defined_vals = dict()
    def construct_parameter_space(self,iterating_parameter,parameter_list):
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
        #print(self.defined_vals)
        self.evaluator = asteval.Interpreter(usersyms=self.defined_vals)

    def get_cost(self):
        self.tot_cost = self.evaluator(self.cost_formula)
        return self.tot_cost
class VerifyAssertions:
    def __init__(self, assertions_formulas):
        self.assertions = assertions_formulas
        self.defined_vals = dict()
    def construct_parameter_space(self,iterating_parameter,parameter_list):
        # add cost values for all parameters in the parameter space
        self.parameter_list = parameter_list
        for i in parameter_list:
            if(i.type != 'composite' and i.type != 'bool' and i.type != 'float'):
                self.defined_vals[i.name] = int(i.temporary_val)
            elif(i.type == 'float'):
                self.defined_vals[i.name] =  float(i.temporary_val)
            elif(i.type =='bool'):
                self.defined_vals[i.name] =  bool(i.temporary_val)
            else:
                for j in i.temporary_val:
                    for k in j:
                        if(k.type != 'composite' and k.type != 'bool'  and k.type != 'float'):
                            self.defined_vals[k.name] =  int(k.temporary_val)
                        elif(k.type == 'float'):
                            self.defined_vals[k.name] =  float(k.temporary_val)
                        elif(k.type =='bool'):
                            self.defined_vals[k.name] =  bool(k.temporary_val)

        self.defined_vals[iterating_parameter.name] = iterating_parameter.temporary_val
        #print(self.defined_vals)
        self.evaluator = asteval.Interpreter(usersyms=self.defined_vals)

    def verify_assertions(self):
        all_asserts_valid = True;
        for i in self.assertions.assertion_list:
            if self.evaluator(i):
                print("Assertion \t<<",i,">>\t holds in current state")
            else:
                print("Assertion \t<<",i,">>\t does NOT in current state")
                all_asserts_valid = False
        return False

