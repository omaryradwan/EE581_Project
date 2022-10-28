# This file defines the Algorithm Class. This class is the parent class of detailed algorithm classes.
#
# All the algorithms should contain the following attributes:
#       variables           --          This is a list of variable class                eg:[bool,float,int]
#       initIterator        --          This is the iterator of algorithm               eg:t, T
#       initIterator        --          The iterator parameter of this variable         eg: t, T
#       initStepSize        --          The default step size of iterator               eg: 0.01
#       initItBound         --          The bound of iterator parameter                 eg: [0, 100]
#       initItFunc          --          The function of step size, default 0.01x        eg: x^2+2x
#
# The algorithm should contain the following functions:
#       UpdateVariables     --          The function used to update variables in one step, return variables

class Algorithm:
    def __init__(self, variables, initIterator, initStepSize, initItBound, initItFunc):
        self.variables = variables
        self.initIterator = initIterator
        self.initStepSize = initStepSize
        self.initItBound = initItBound
        self.initItFunc = initItFunc

    def UpdateVariables(self):
        pass



class SimulatedAnnealing(Algorithm):
    def __init__(self, variables, initIterator, initStepSize, initItBound, initItFunc)
        super()..__init__(variables, initIterator)

    def UpdateVariables(self):
        #TBD
        return self.variables

class ParticleSwarm(Algorithm):
    def __init__(self, variables, initIterator, initStepSize, initItBound, initItFunc)
        super()..__init__(variables, initIterator)

    def UpdateVariables(self):
        #TBD
        return self.variables

class GeneticEvo(Algorithm):
    def __init__(self, variables, initIterator, initStepSize, initItBound, initItFunc)
        super()..__init__(variables, initIterator)

    def UpdateVariables(self):
        #TBD
        return self.variables