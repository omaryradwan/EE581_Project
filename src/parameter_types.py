# This file defines type classes.
#
# One Type class should have the following attributes:
#       name                --  
#       wrt                 --  
#       init_value          --  The initial value of variable from user
#       value_range         --  The bounds of the variable from user            eg: [[1,3]], [[1,3],[4,7]]
#       upper_bound         --  The dependent bounds of the variable from user  eg: [[-a, a^2], [a, a+1]]
#       lower_bound         --  The discrete value of variable                  eg: 1, 2, [1,3,5]
#
#
#  One Type class should have the following functions:
#       transformIntoDiscrete()         --          Transform a given value into the discrete field, return the discrete value
#       transformBack()                 --          Transform a given discrete value into tyoed field, return the typed value
#       updatediscVal()                 --          Update discrete value by given value
#       updatetmpVal()                  --          Update tmporary value by given value


class Int_Parameter:
    self.name = name
    self.wrt = wrt
    self.init_value = init_value
    self.value_range = value_range
    self.upper_bound = upper_bound
    self.lower_bound = lower_bound
    self.step = step
    self.trans_function = trans_function
    def __init__(self, name, value_range, upper_bound, lower_bound,step,trans_function, init_value = None, wrt = False):
        self.name = name
        self.wrt = wrt
        self.init_value = init_value
        self.value_range = value_range
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.step = step
        self.trans_function = trans_function
    def items():
        return __dict__

    def transformIntoDiscrete(val):
        return val
    
    def transformBack(val):
        return val

class Bool_Parameter:
    def __init__(self, name, value_range, upper_bound, lower_bound,step,trans_function, init_value = None, wrt = False):
        self.name = name
        self.wrt = wrt
        self.init_value = init_value
        self.value_range = value_range
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.step = step
        self.trans_function = trans_function
    
    def transformIntoDiscrete(val):
        if val:
            return 1
        return 0
    
    def transformBack(val):
        if val == 1:
            return True
        return False

class Float_Parameter:
    def __init__(self, name, value_range, upper_bound, lower_bound,step,trans_function, init_value = None, wrt = False):
        self.name = name
        self.wrt = wrt
        self.init_value = init_value
        self.value_range = value_range
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.step = step
        self.trans_function = trans_functio

    def transformIntoDiscrete(val):
        #TBD
    
    def transformBack(val):
        #TBD

parameter_types = {"Int_Parameter" : Int_Parameter, "Bool_Paramter" : Bool_Parameter, "Float_Parameter" : Float_Parameter}
