# This file defines type classes.
#
# One Type class should have the following attributes:
#       name                --  
#       wrt                 --  
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
import ast

class Int_Parameter:
    def __init__(self, name, value_range, upper_bound, lower_bound, init_value = None):
        self.type = 'int'
        self.name = name
        self.init_value = init_value
        self.temporary_val = init_value
        self.value_range = value_range
        self.upper_bound = int(upper_bound)
        self.lower_bound = int(lower_bound)
        self.discrete_val = 0


    def TransformIntoDiscrete(self, val):
        return val
    
    def TransformBack(self, val):
        return val

    def UpdatediscVal(self, val):
        self.discrete_val = val
    
    def UpdatetmpVal(self, val):
        self.temporary_val = val

    def GenRandomNeighbor(self, name):
        new_val = random.randint(self.lower_bound, self.upper_bound)
        return Int_Parameter(new_name, self.value_range, self.upper_bound, self.lower_bound,
                                                self.step, self.trans_function, new_val, self.wrt)

    def GenRandomNeighbors(self, neighbor_num):
        neighbor_list = []
        for i in range(neighbor_num - 1):
            new_name = self.name + "_next_" + str(i)
            neighbor_list.append(self.GenRandomNeighbor(new_name))
        return neighbor_list
        

class Bool_Parameter:
    def __init__(self, name, value_range, upper_bound, lower_bound, true_weight, false_weight, init_value = None):
        self.type = 'bool'
        self.name = name
        self.init_value = init_value
        self.temporary_val = init_value
        self.value_range = value_range
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.discrete_val = 0
        self.true_weight = true_weight
        self.false_weight = false_weight
    
    def TransformIntoDiscrete(self, val):
        if val:
            return 1
        return 0
    
    def TransformBack(self, val):
        if val == 1:
            return True
        return False

    def UpdatediscVal(self, val):
        self.discrete_val = val

    def UpdatetmpVal(self, val):
        self.temporary_val = val

    def GenRandomNeighbor(self, name):
        new_val = random.choice([True, False])
        return Bool_Parameter(new_name, self.value_range, self.upper_bound, self.lower_bound, self.true_weight, self.false_weight, self.step, self.trans_function, new_val, self.wrt)

    def GenRandomNeighbors(self, neighbor_num):
        neighbor_list = []
        for i in range(neighbor_num - 1):
            new_name = self.name + "_next_" + str(i)
            neighbor_list.append(self.GenRandomNeighbor(new_name))
        return neighbor_list

class Float_Parameter:
    def __init__(self, name, value_range, upper_bound, lower_bound, init_value = None):
        self.type = 'float'
        self.name = name
        self.init_value = init_value
        self.temporary_val = init_value
        self.value_range = value_range
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.discrete_val = 0

    def TransformIntoDiscrete(self, val):
        # TBD
        # Currently I keep three digits after the dot '.'
        # Eg: 0.4777 -> {477, -3}, 123123.23 -> {123123230, -3}
        float_transed = float(format(val, '.3f'))
        return {int(float_transed*1000), -3}
    
    def TransformBack(self, val):
        return float(val)/1000

    def UpdatediscVal(self, val):
        self.discrete_val = val

    def UpdatetmpVal(self, val):
        self.temporary_val = val
    
    def GenRandomNeighbor(self, name):
        new_val = random.uniform(self.lower_bound, self.upper_bound)
        return Float_Parameter(name, self.value_range, self.upper_bound, self.lower_bound,
                                                self.step, self.trans_function, new_val, self.wrt)

    def GenRandomNeighbors(self, neighbor_num):
        neighbor_list = []
        for i in range(neighbor_num - 1):
            new_name = self.name + "_next_" + str(i)
            neighbor_list.append(self.GenRandomNeighbor(new_name))
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

    def GenRandomNeighbor(self, name):
        new_child_list = []
        for child in self.children_list:
            new_child_list.append(child.GenRandomNeighbor())
        return Composite_Parameter(name, children_list = new_child_list)


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

    def GenRandomNeighbors(self, neighbor_num):
        neighbor_list = []
        for i in range(neighbor_num - 1):
            new_name = self.name + "_next_" + str(i)
            neighbor_list.append(self.GenRandomNeighbor(name))
        return neighbor_list


class Iterating_Parameter:
    def __init__(self, name, init_value, bound, step, step_function):
        self.type = 'iterating'
        self.name = name
        self.init_value = init_value
        self.bound = bound
        self.step = step
        self.step_function = step_function
        self.temporary_val = init_value

    def IsOverBound(self):
        if self.temporary_val > bound:
            return False
        return True

    def Iterate(self):
        # self.temporary_val = ast_calculate(self.step_function, step)
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
    # print(parameters)
    type_name = parameters['type']
    if type_name == 'int':
        var = Int_Parameter(parameters['name'], parameters['value_range'], parameters['upper_bound'],
                             parameters['lower_bound'], parameters['init_value'])
        return var
    elif type_name == 'bool':
        return Bool_Parameter(parameters['name'], parameters['value_range'], parameters['upper_bound'], parameters['lower_bound'],parameters['true_weight'],parameters['false_weight'],
                               parameters['init_value'])
    elif type_name == 'float':
        return Float_Parameter(parameters['name'], parameters['value_range'], parameters['upper_bound'],
                             parameters['lower_bound'], parameters['init_value'])
    elif type_name == 'composite':
        return Composite_Parameter(parameters['name'], parameters['values'])
    print("Error: " + type_name + " type does not exist, exiting")

def InitIteratingVariable(parameters):
    return Iterating_Parameter(parameters['name'], parameters['init_value'], parameters['bound'],
                                parameters['step'], parameters['step_function'])

def InitAssertions(parameters):
    return Assertions(parameters['values'])
