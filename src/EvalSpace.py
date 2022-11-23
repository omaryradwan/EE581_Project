import ast
import asteval
import sympy
from sympy import *
import random
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
        # print(self.defined_vals)
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
            # print(i)
            if self.evaluator(i):
                # print("Assertion \t<<",i,">>\t holds in current state")
                continue
            else:
                # print("Assertion \t<<",i,">>\t does NOT in current state")
                all_asserts_valid = False
        # print(all_asserts_valid)
        return all_asserts_valid

    def valid_parameter_range(self, iterating_parameter, parameter_list, target_parameter):

        local_parameter_list = list()
        param_to_symbol_dict = dict()

        #adding iterating parameter as a symbol
        param_to_symbol_dict[iterating_parameter.name] = symbols(iterating_parameter.name, integer = True)

        #adding all other parameters from parameter_list to symbols, as well as storing them privately to do stuff with them
        for i in parameter_list:
            if i.type == 'float':
                i.SetTransformed(i.temporary_val)
            #if its composite, we don't want to add the whole thing, its components
            if i.type == "composite":
                for j in i.temporary_val:
                    for k in j:
                        parameter_list.append(k)
                continue
            #create a symbol and add a top level symbol to our list
            param_to_symbol_dict[i.name] = symbols(i.name, integer = True)
            local_parameter_list.append(i)

        #go through the available assertioms, and if our target_parameter is in their, pull it in
        eq_dict = dict()
        bound_eq_str = target_parameter.lower_bound + " < " + target_parameter.name + " < "  + target_parameter.upper_bound
        # bound_solve = sympify(bound_eq_str)
        for i in self.formulas.assertion_list:
            for j in sympify(i).free_symbols:
                if str(j) == str(param_to_symbol_dict[target_parameter.name]):
                    eq_dict[i] = sympify(i, evaluate=False)


        #go through all the assertions and subsitutute all the values for the symbols(first for iterating parameter, then for the rest of them, as long as they're not target parameter)
        valid_interval_list = list()
        for i in eq_dict.keys():
            maximum_exp = 0
            eq_dict[i] = eq_dict[i].subs(param_to_symbol_dict[iterating_parameter.name], iterating_parameter.temporary_val)

            for param in local_parameter_list:
                if param.name == target_parameter.name:
                    continue
                if(param.type == "float"):
                    eq_dict[i] = eq_dict[i].subs(param.name, param.sig);
                    maximum_exp += param.sig
                elif (param.type == "int"):
                    eq_dict[i] = eq_dict[i].subs(param.name, param.temporary_val)
        valid_interval_list.append(solveset(eq_dict[i], target_parameter.name, domain=S.Integers))

        interval = Interval(int(target_parameter.lower_bound), int(target_parameter.upper_bound))
        for i in valid_interval_list:
            interval = interval.intersect(i)

        print("valid interval for target parameter", target_parameter.name)
        print(interval)
        #print(interval[0], interval[len(interval)])


class EvalStepFunction(EvalUtils):
    def __init__(self, step_function, iterating_parameter):
        super().__init__(step_function, iterating_parameter, [])

    def get_step(self):
        self.step = self.evaluator(self.formulas)
        return self.step
