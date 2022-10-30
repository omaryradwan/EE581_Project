# This file defines the Algorithm Class. This class is the parent class of detailed algorithm classes.
#
# All the algorithms should contain the following attributes:
#       variable_list       --          This is a list of variable class                eg: [v1, v2, v3]
#       variable_dict        --         This is dict of N poits of each variable        eg: [v1: [1,2,3], v2: [3,4,5], v3: [3,5,1]]
#       initIterator        --          This is the iterator of algorithm               eg: t, T
#       initStepSize        --          The default step size of iterator               eg: 0.01
#       initItBound         --          The bound of iterator parameter                 eg: [0, 100]
#       initItFunc          --          The function of step size, default 0.01x        eg: x^2+2x
#       cost_function       --          Then costfunction of variables                  eg: x^2+y^2
#
# The algorithm should contain the following functions:
#       UpdateVariables     --          The function used to update variables in one step, return variables
#       CreateVariableDict  --          Randomly slelect neighbor of initial point to create initial dict, each variable n points.

class Algorithm:
    def __init__(self, variable_list, initIterator, initStepSize, initItBound, initItFunc, cost_function):
        self.variable_list = variable_list
        self.initIterator = initIterator
        self.initStepSize = initStepSize
        self.initItBound = initItBound
        self.initItFunc = initItFunc
        self.cost_function = cost_function

    def UpdateVariables(self):
        pass

    def CreateVariableDict(self):
        pass



class SlefDefinedAlgorithm(Algorithm):
    def __init__(self, variable_list, initIterator, initStepSize, initItBound, initItFunc, cost_function):
        super()..__init__(variable_list, initIterator)

    def UpdateVariables(self):
        #TBD
        return self.variables


class SimulatedAnnealing(Algorithm):
    def __init__(self, variable_list, initIterator, initStepSize, initItBound, initItFunc, cost_function):
        super()..__init__(variable_list, initIterator)

    def UpdateVariables(self):
        #TBD
        return self.variables

class ParticleSwarm(Algorithm):
    def __init__(self, variable_list, initIterator, initStepSize, initItBound, initItFunc, cost_function):
        super()..__init__(variable_list, initIterator)

    def UpdateVariables(self):
        #TBD
        return self.variables

class GeneticEvo(Algorithm):
    def __init__(self, variable_list, initIterator, initStepSize, initItBound, initItFunc, cost_function)
        super()..__init__(variable_list, initIterator)

    def UpdateVariables(self):
        #TBD
        return self.variables
