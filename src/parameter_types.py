# This file defines type classes.
#
# Type class have the following attributes: Int, Bool, Float, Composite
#       name                --  The name of variable                                    eg: param_A
#       type                --  The type of variable                                    eg: int, float, bool
#       init_value          --  The initial value of variable from user                 eg: 1.3, False, 2
#       temporary_val       --  The temporary value of variable, updated every step     eg: 1.3, False, 2
#       value_set           --  The valid set of the variable                           eg: [1,2,...,10]
#       upper_bound         --  The upper const bound of variable                       eg: -10, -5
#       lower_bound         --  The lower const bound of variable                       eg: 10, 20
#       discrete_val        --  The temporary discrete value                            eg: 1, 0, 2
#       true_weight         --  The value of bool variable when it is true              eg: 10, 20
#       false_weight        --  The value of bool variable when it is true              eg: 10, 50
#
# Type class should have the following functions:
#       __init__                            --          Initialize the typed parameter
#       UpdateValueSet()                    --          Update value set by given set
#       UpdatediscVal()                     --          Update discrete value by given value
#       UpdatetmpVal()                      --          Update tmporary value by given value
#       GenRandomNeighbor()                 --          Generate 1 random neighbor
#       GenRandomNeighbors()                --          Generate N random neighbors
#       GetChildrenFromJson()               --          Initialize the composite children from JSON


import random
import numpy as np
import EvalSpace
import math
import time

class Int_Parameter():
    def __init__(self, name, upper_bound, lower_bound, init_value = None):
        self.name = name
        self.type = 'int'
        if init_value != None:
            self.init_value = init_value
        else:
            self.init_value = random.choice(np.arange(int(lower_bound), int(upper_bound),1).tolist())
        self.temporary_val = random.choice(np.arange(int(lower_bound), int(upper_bound),1).tolist())
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
        # print(weights)
        # print(assertions_set)
        new_val = random.choices(assertions_set, weights=weights.tolist(), k=1)[0]
        # random.seed(time.time())
        # new_val = random.choice(assertions_set)

        # print(new_val)
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
    def __init__(self, name, true_weight, false_weight, init_value = None):
        self.type = 'bool'
        self.name = name
        if init_value != None:
            self.init_value = init_value
        else:
            self.init_value = random.choice([True,False])
        self.temporary_val = random.choice([True,False])
        self.true_weight = true_weight
        self.false_weight = false_weight
        self.value_set = [False, True]

    def UpdateValueSet(self, value_set):
        self.value_set = value_set

    def UpdatetmpVal(self, val):
        self.temporary_val = val

    def GenRandomNeighbor(self, name, assertions, iterating_parameter, variable_list):
        assertions_set = assertions.get_valid_interval(iterating_parameter, variable_list, self)
        # print("bools only", assertions_set)
        if(np.amax(assertions_set) == int(self.true_weight) - 1):
            new_val = True
        elif(np.amin(assertions_set) == int(self.false_weight) - 1):
            new_val = False
        else:
            new_val = random.choice(self.value_set)
        new_variable = Bool_Parameter(name, self.true_weight, self.false_weight, self.init_value)
        # print(new_val, self.value_set)
        new_variable.UpdatetmpVal(new_val)
        return new_variable

    def GenRandomNeighbors(self, neighbor_num, assertions, iterating_parameter, variable_list):
        neighbor_list = []
        for i in range(neighbor_num):
            new_name = self.name
            neighbor_list.append(self.GenRandomNeighbor(new_name, assertions, iterating_parameter, variable_list))
        return neighbor_list

class Float_Parameter:
    def __init__(self, name, upper_bound, lower_bound, digits, init_value = None):
        self.type = 'float'
        self.name = name
        if init_value != None:
            self.init_value = init_value
        else:
            self.init_value = random.choice(np.arange(float(lower_bound), float(upper_bound),1.0).tolist())
        self.temporary_val = random.choice(np.arange(float(lower_bound), float(upper_bound),1.0).tolist())
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
        # print(self.value_set)
        new_val = random.choice(self.value_set)
        new_variable = Float_Parameter(name, self.upper_bound, self.lower_bound, self.init_value, self.digits)
        new_variable.UpdatetmpVal(new_val)
        # print(new_val)
        # print(new_variable.temporary_val)
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
        for i in range(neighbor_num):
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

parameter_types = {"int" : Int_Parameter,
                    "bool" : Bool_Parameter,
                    "float" : Float_Parameter,
                    "composite": Composite_Parameter}


def InitTypedVariable(parameters):
    type_name = parameters['type']
    if type_name == 'int':
        var = Int_Parameter(parameters['name'], parameters['upper_bound'],parameters['lower_bound'])
        return var
    elif type_name == 'bool':
        return Bool_Parameter(parameters['name'],parameters['true_weight'],parameters['false_weight'])
    elif type_name == 'float':
        return Float_Parameter(parameters['name'], parameters['upper_bound'], parameters['lower_bound'],parameters['digits'])
    elif type_name == 'composite':
        return Composite_Parameter(parameters['name'], parameters['values'])
    print("Error: " + type_name + " type does not exist, exiting")

def InitIteratingVariable(parameters):
    return Iterating_Parameter(parameters['name'], parameters['init_value'], parameters['bound'],
                                parameters['step'], parameters['step_function'])

def InitAssertions(parameters):
    return Assertions(parameters['values'])
