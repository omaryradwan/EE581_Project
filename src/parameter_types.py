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
parameter_types = {"Int_Parameter" : Int_Parameter, "Bool_Paramter" : Bool_Parameter, "Float_Parameter" : Float_Parameter}
