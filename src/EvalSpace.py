import asteval
import numpy as np
import random
from functools import reduce
from sympy import *
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

    def get_valid_interval(self,iterating_parameter, parameter_list, target_parameter):
        eq_list = list()
        for i in self.formulas.assertion_list:
            if target_parameter.name in i:
                eq_list.append(i)
        for i in set(parameter_list):
            if i.type == 'float':
                i.SetTransformed(i.temporary_val)
            if i.type == "composite":
                for j in i.temporary_val:
                    for k in j:
                        parameter_list.append(k)
                # parameter_list.remove(i)
                continue
            parameter_list.append(i)

        valid_interval_list = list()
        initial_valid_bound = None
        if target_parameter.type == "int":
            initial_valid_bound =  np.arange(target_parameter.lower_bound, target_parameter.upper_bound, 1)
        elif target_parameter.type == "bool":
            initial_valid_bound = np.arange(int(target_parameter.false_weight), int(target_parameter.true_weight), 1)
        valid_interval_list.append(initial_valid_bound)

        for equation_inst in eq_list:
            equation_inst = equation_inst.replace(iterating_parameter.name, str(iterating_parameter.temporary_val))
            for param in set(parameter_list):
                if param.type == 'composite':
                    continue
                if param.name == target_parameter.name:
                    continue
                if param.type == "float" :
                    param.SetTransformed(param.temporary_val)
                    equation_inst = equation_inst.replace(param.name, str(param.temporary_val))
                elif param.type == "int":
                    equation_inst = equation_inst.replace(param.name, str(param.temporary_val))
                if param.type == "bool":
                    if param.temporary_val:
                        equation_inst = equation_inst.replace(param.name, str(param.true_weight))
                    else:
                        equation_inst = equation_inst.replace(param.name, str(param.false_weight))

            eq = lambdify(target_parameter.name, equation_inst)
            if target_parameter.type is not "bool":
                valid_bound_arr =  np.arange(target_parameter.lower_bound, target_parameter.upper_bound, 1)
            else:
                # print(equation_inst)
                valid_bound_arr =  np.arange(int(target_parameter.false_weight) - 1, int(target_parameter.true_weight) + 1, 1)
            valid_bound_arr_candidate = eq(valid_bound_arr)

            #for all solution or no solution
            if(type(valid_bound_arr_candidate) == bool):
                if valid_bound_arr_candidate == False :
                    return []
                if(valid_bound_arr_candidate == True):
                    continue
            if(valid_bound_arr_candidate[0].dtype == bool):
                valid_bound_arr = valid_bound_arr[valid_bound_arr_candidate == True]
                if target_parameter.type == 'bool':
                    # print(valid_bound_arr)
                    if len(valid_bound_arr) == 0:
                        return [ int(target_parameter.false_weight) ]

                # print(valid_bound_arr)
            else:
                valid_bound_arr = valid_bound_arr_candidate

            valid_interval_list.append(valid_bound_arr)

        fully_valid_interval = reduce(np.intersect1d, valid_interval_list)

        if len(fully_valid_interval.tolist()) == 0:
            return initial_valid_bound.tolist()
        return(fully_valid_interval.tolist())


class EvalStepFunction(EvalUtils):
    def __init__(self, step_function, iterating_parameter):
        super().__init__(step_function, iterating_parameter, [])

    def get_step(self):
        self.step = self.evaluator(self.formulas)
        return self.step
