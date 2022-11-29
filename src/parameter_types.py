# This file defines type classes.
#
# One Type class should have the following attributes:
#       name                --  The name of the variable                                eg: param_A
#       init_value          --  The initial value of variable from user                 eg: 1.3, False, 2
#       temporary_val       --  The temporary value of variable, updated every step     eg: 1.3, False, 2
#       value_range         --  The bounds of the variable from user                    eg: [[1,3]], [[1,3],[4,7]]
#       upper_bound         --  The dependent bounds of the variable from user          eg: [[-a, a^2], [a, a+1]]
#       lower_bound         --  The discrete value of variable                          eg: 1, 2, [1,3,5]
#       discrete_val        --  The current discrete value                              eg: 3, 4, 5
#
#
#  One Type class should have the following functions:
#       TransformIntoDiscrete()         --          Transform a given value into the discrete field, return the discrete value
#       TransformBack()                 --          Transform a given discrete value into tyoed field, return the typed value
#       UpdatediscVal()                 --          Update discrete value by given value
#       UpdatetmpVal()                  --          Update tmporary value by given value
#       GenRandomNeighbors()            --          Generate N random neighbors


import random
import numpy as np
import EvalSpace
import math

class Int_Parameter():
    def __init__(self, name, upper_bound, lower_bound, init_value):
        self.name = name
        self.type = 'int'
        self.init_value = int(init_value)
        self.temporary_val = int(init_value)
        self.upper_bound = int(upper_bound)
        self.lower_bound = int(lower_bound)
        self.value_set = self.InitValueSet([[self.lower_bound, self.upper_bound]])

    # This function takes a list of interval ends (integer) and return a set contain all unique points in these intervals
    # eg: InitValueSet([[1,3], [2,5]]) will return a list [1,2,3,4,5].
    # Attention: Make sure the interval_ends_list contain at least one point.
    def InitValueSet(self, interval_ends_list):
        value_list = []
        for interval_pair in interval_ends_list:
            left_end = interval_pair[0]
            right_end = interval_pair[1]
            for val in range(left_end, right_end):
                value_list.append(val)
        return list(set(value_list))

    def UpdateValueSet(self, value_set):
        self.value_set = value_set

    def UpdatetmpVal(self, val):
        self.temporary_val = val

    def GenRandomNeighbor(self, name, assertions, iterating_parameter, variable_list):
        random.seed()
        assertions_set = assertions.get_valid_interval(iterating_parameter, variable_list, self)
        self.UpdateValueSet(assertions_set)
        assertion_arr = np.array(assertions_set)
        assertions_set.sort(key = lambda x: abs(x - self.temporary_val))
        weight_arr = np.arange(0,len(assertions_set))
        len_arr = len(assertions_set)
        calc_dist = lambda x: (len_arr - x)**2
        vec_len_arr = np.vectorize(calc_dist)
        weights = vec_len_arr(weight_arr)
        new_val = random.choices(assertions_set, weights=weights.tolist(), k=1)[0]

        # new_val = random.choice(assertions_set)
        new_variable = Int_Parameter(name, self.upper_bound, self.lower_bound, self.init_value)
        new_variable.UpdatetmpVal(new_val)
        return new_variable


    def GenRandomNeighbors(self, neighbor_num, assertions, iterating_parameter, variable_list):
        neighbor_list = []
        for i in range(neighbor_num):
            new_name = self.name
            neighbor_list.append(self.GenRandomNeighbor(new_name, assertions, iterating_parameter, variable_list))
        return neighbor_list


class Bool_Parameter:
    def __init__(self, name, true_weight, false_weight, init_value):
        self.type = 'bool'
        self.name = name
        self.init_value = init_value
        self.temporary_val = init_value
        self.true_weight = true_weight
        self.false_weight = false_weight
        self.value_set = [false_weight, true_weight]


    def UpdateValueSet(self, value_set):
        self.value_set = value_set

    def UpdatetmpVal(self, val):
        self.temporary_val = val

    def GenRandomNeighbor(self, name, assertions, iterating_parameter, variable_list):
        assertions_set = assertions.get_valid_interval(iterating_parameter, variable_list, self)
        self.UpdateValueSet(assertions_set)
        new_val = random.choice(self.value_set)
        new_variable = Bool_Parameter(name, self.true_weight, self.false_weight, self.init_value)
        new_variable.UpdatetmpVal(new_val)
        return new_variable

    def GenRandomNeighbors(self, neighbor_num, assertions, iterating_parameter, variable_list):
        neighbor_list = []
        for i in range(neighbor_num):
            new_name = self.name
            neighbor_list.append(self.GenRandomNeighbor(new_name, assertions, iterating_parameter, variable_list))
        return neighbor_list

class Float_Parameter:
    def __init__(self, name, upper_bound, lower_bound, init_value, digits):
        self.type = 'float'
        self.name = name
        self.init_value = float(init_value)
        self.temporary_val = float(init_value)
        self.upper_bound = float(upper_bound)
        self.lower_bound = float(lower_bound)
        self.discrete_val = 0
        self.value_set = self.InitValueSet([[self.lower_bound, self.upper_bound]])
        self.digits = digits

    # This function takes a list of interval ends and return a set contain all unique points in these intervals
    # eg: InitValueSet([[1.5,3], [2,5]]) will return a list [2,3,4,5].
    # Attention: Make sure the interval_ends_list contain at least one point.
    def InitValueSet(self, interval_ends_list):
        value_list = []
        for interval_pair in interval_ends_list:
            left_end = math.ceil(interval_pair[0])
            right_end = math.floor(interval_pair[1]) ##[1.2323, 1.4444]
            for val in range(left_end, right_end):
                value_list.append(val)
        return list(set(value_list))

    def UpdateValueSet(self, value_set):
        self.value_set = value_set

    def SetTransformed(self, num):
        decimal_places = 18
        num = round(num, -int(math.floor(math.log10(abs(num)))) + 2)
        num_str = str(f'{num:.{decimal_places}f}')
        parts = num_str.split('.', 2)
        decimal = parts[1] if len(parts) > 1 else ''
        exp = -len(decimal)
        digits = parts[0].lstrip('0') + decimal
        trimmed = digits.rstrip('0')
        exp += len(digits) - len(trimmed)
        sig = int(trimmed) if trimmed else 0
        self.exp = exp
        self.sig = sig

    def UpdatediscVal(self, val):
        self.discrete_val = val

    def UpdatetmpVal(self, val):
        self.temporary_val = float(val)

    def GenRandomNeighbor(self, name, assertions, iterating_parameter, variable_list):
        random.seed()
        assertions_set = assertions.get_valid_interval(iterating_parameter, variable_list, self)
        self.UpdateValueSet(assertions_set)
        new_val = random.choice(self.value_set)
        new_variable = Float_Parameter(name, self.upper_bound, self.lower_bound, self.init_value, self.digits)
        new_variable.UpdatetmpVal(new_val)
        return new_variable

    def GenRandomNeighbors(self, neighbor_num, assertions, iterating_parameter, variable_list):
        neighbor_list = []
        for i in range(neighbor_num):
            new_name = self.name
            neighbor_list.append(self.GenRandomNeighbor(new_name, assertions, iterating_parameter, variable_list))
        return neighbor_list

class Composite_Parameter:
    def __init__(self, name, children_json=None, children_list=None):
        self.type = 'composite'
        self.name = name
        if children_json != None:
            self.children_list = self.GetChildrenFromJson(children_json)
            self.temporary_val = self.children_list
        else:
            self.children_list = children_list
            self.temporary_val = self.children_list

    def GetChildrenFromJson(self, children_json):
        children_list = []
        for children in children_json:
            # print("tmp children are:", children)
            tmp_children_group = []
            for child in children:
                # print("tmp child is", child)
                child_json = children[child]
                # print(child_json)
                tmp_children_group.append(InitTypedVariable(child_json))
            children_list.append(tmp_children_group)
        return children_list

    def GenRandomNeighbor(self, name, assertions, iterating_parameter, variable_list):
        new_child_list = []
        for child_group in self.children_list:
            new_child_group = []
            for child in child_group:
                new_child_group.append(child.GenRandomNeighbor(child.name, assertions, iterating_parameter, variable_list))
            new_child_list.append(new_child_group)
        return Composite_Parameter(name, children_list = new_child_list)


    def GenRandomNeighbors(self, neighbor_num, assertions, iterating_parameter, variable_list):
        neighbor_list = []
        for i in range(neighbor_num - 1):
            new_name = self.name
            neighbor_list.append(self.GenRandomNeighbor(new_name, assertions, iterating_parameter, variable_list))
        return neighbor_list


class Iterating_Parameter:
    def __init__(self, name, init_value, bound, step, step_function):
        self.type = 'iterating'
        self.name = name
        self.init_value = float(init_value)
        self.bound = float(bound)
        self.step = float(step)
        self.temporary_val = float(init_value)
        self.step_function = EvalSpace.EvalStepFunction(step_function, self)

    def IsOverBound(self):
        if self.temporary_val > self.bound:
            return True
        return False

    def Iterate(self):
        self.step_function.construct_parameter_space(self,[])
        self.temporary_val = self.temporary_val + self.step_function.get_step()
        return


class Assertions:
    def __init__(self, assertion_list):
        self.assertion_list = assertion_list

    def AreAssertionsSatisfied():
        # TBD
        # Evaluate every assertion value and if any violated, return false.
        return true

parameter_types = {"int" : Int_Parameter,
                    "bool" : Bool_Parameter,
                    "float" : Float_Parameter,
                    "composite": Composite_Parameter}


def InitTypedVariable(parameters):
    type_name = parameters['type']
    if type_name == 'int':
        var = Int_Parameter(parameters['name'], parameters['upper_bound'],
                             parameters['lower_bound'], parameters['init_value'])
        return var
    elif type_name == 'bool':
        return Bool_Parameter(parameters['name'],parameters['true_weight'],parameters['false_weight'],
                               parameters['init_value'])
    elif type_name == 'float':
        return Float_Parameter(parameters['name'], parameters['upper_bound'], parameters['lower_bound'],
                                parameters['init_value'], parameters['digits'])
    elif type_name == 'composite':
        return Composite_Parameter(parameters['name'], parameters['values'])
    print("Error: " + type_name + " type does not exist, exiting")

def InitIteratingVariable(parameters):
    return Iterating_Parameter(parameters['name'], parameters['init_value'], parameters['bound'],
                                parameters['step'], parameters['step_function'])

def InitAssertions(parameters):
    return Assertions(parameters['values'])
