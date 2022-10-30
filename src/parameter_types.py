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

class Int_Parameter:
    def __init__(self, name, value_range, upper_bound, lower_bound,step,trans_function, init_value = None, wrt = False):
        self.name = name
        self.wrt = wrt
        self.init_value = init_value
        self.temporary_val = init_value
        self.value_range = value_range
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.step = step
        self.trans_function = trans_function
        self.discrete_val = 0


    def TransformIntoDiscrete(self, val):
        return val
    
    def TransformBack(self, val):
        return val

    def UpdatediscVal(self, val):
        self.discrete_val = val
    
    def UpdatetmpVal(self, val):
        self.temporary_val = val

    def GenRandomNeighbors(self, neighbor_num):
        neighbor_list = [self]
        for i in range(neighbor_num - 1):
            new_name = self.name + "_next_" + str(i)
            new_val = random.randint(self.lower_bound, self.upper_bound)
            neighbor_list.append(Int_Parameter(new_name, self.value_range, self.upper_bound, self.lower_bound,
                                                self.step, self.trans_function, new_val, self.wrt))
        
        return neighbor_list
        

class Bool_Parameter:
    def __init__(self, name, value_range, upper_bound, lower_bound,step,trans_function, init_value = None, wrt = False):
        self.name = name
        self.wrt = wrt
        self.init_value = init_value
        self.temporary_val = init_value
        self.value_range = value_range
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.step = step
        self.trans_function = trans_function
        self.discrete_val = 0
    
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

    def GenRandomNeighbors(self, neighbor_num):
        neighbor_list = []
        for i in range(neighbor_num - 1):
            new_name = self.name + "_next_" + str(i)
            new_val = random.choice([True, False])
            neighbor_list.append(Int_Parameter(new_name, self.value_range, self.upper_bound, self.lower_bound,
                                                self.step, self.trans_function, new_val, self.wrt))
        
        return neighbor_list

class Float_Parameter:
    def __init__(self, name, value_range, upper_bound, lower_bound,step,trans_function, init_value = None, wrt = False):
        self.name = name
        self.wrt = wrt
        self.init_value = init_value
        self.temporary_val = init_value
        self.value_range = value_range
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.step = step
        self.trans_function = trans_functio
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
    
    def GenRandomNeighbors(self, neighbor_num):
        neighbor_list = []
        for i in range(neighbor_num - 1):
            new_name = self.name + "_next_" + str(i)
            new_val = random.uniform(self.lower_bound, self.upper_bound)
            neighbor_list.append(Int_Parameter(new_name, self.value_range, self.upper_bound, self.lower_bound,
                                                self.step, self.trans_function, new_val, self.wrt))
        
        return neighbor_list

parameter_types = {"Int_Parameter" : Int_Parameter, "Bool_Paramter" : Bool_Parameter, "Float_Parameter" : Float_Parameter}

#   Example Coding:
#       var1 = Float_Parameter('motor_one', [-180, 180], ...)
#       var2 = Float_Parameter('motor_two', [-180, 180], ...)
#       var3 = Float_Parameter('motor_three', [-180, 180], ...)
#       var4 = Float_Parameter('motor_four', [-180, 180], ...)
#       vars = [var1, var2, var3, var4]
#       Algorithm.UpdateVariables(vars, iterator, stepsize, trans_function, cost_function)
#
#   Inside the UpdateVariables function, we call TransformBack() to get typed val and measure the cost function
#   We call UpdatediscVal() to update the discrete value of variables 

def InitTypedVariable(type_name, parameters):
    if type_name == 'Int_Parameter':
        var = Int_Parameter(parameters['name'], parameters['value_range'], parameters['upper_bound'],
                             parameters['lower_bound'], parameters['step'], parameters['trans_function'],
                             parameters['init_value'], parameters['wrt'])
        return var
    elif type_name == 'Bool_Paramter':
        return Bool_Parameter(parameters['name'], parameters['value_range'], parameters['upper_bound'],
                             parameters['lower_bound'], parameters['step'], parameters['trans_function'],
                             parameters['init_value'], parameters['wrt'])
    elif type_name == 'Float_Parameter':
        return Float_Parameter(parameters['name'], parameters['value_range'], parameters['upper_bound'],
                             parameters['lower_bound'], parameters['step'], parameters['trans_function'],
                             parameters['init_value'], parameters['wrt'])
    print("Error: " + type_name + " type does not exist, exiting")