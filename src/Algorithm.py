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
#       variable_num        --          The number of variables                         eg: 3
#       search_neighbor_num --          The number of neighbors to check                eg: 10
#       end_requirements    --          The ending requirements of algorithms           eg: 
#
# The algorithm should contain the following functions:
#       UpdateVariables     --          The function used to update variables in one step, return variables
#       CreateVariableDict  --          Randomly slelect neighbor of initial point to create initial dict, each variable n points.

class Algorithm:
    def __init__(self, variable_list, cost_function):
        self.variable_list = variable_list
        # self.initIterator = initIterator
        # self.initStepSize = initStepSize
        # self.initItBound = initItBound
        # self.initItFunc = initItFunc
        self.cost_function = cost_function
        self.variable_num = len(variable_list)
        self.search_neighbor_num = 10   # TO DO: Set the number 10 to a parameter in __init__
        self.name = ''
        # TO DO: ADD attribute end_requirements


    def UpdateVariables(self):
        pass

    def CreateVariableDict(self):
        new_variable_list = []      #[[1,1.4,1.6],[7,7.3,7.7],[10,10.1,10.6]]
        for tmp_variable in range(self.variable_list):
            tmp_new_list = tmp_variable.GenRandomNeighbors(self.search_neighbor_num)
            new_variable_list.append(tmp_new_list)
        return new_variable_list

    def CheckEndRequirements(self):
        pass

    def Solve(self):
        pass


class SelfDefinedAlgorithm(Algorithm):
    def __init__(self, variable_list, cost_function):
        super().__init__(variable_list, cost_function)
        self.name = 'Self Defined Algorithm'

    def UpdateVariables(self):
        new_variable_list = self.CreateVariableDict()
        cost_val_list = []
        possible_val_list = []      #[[1,7,10],[1.4,7.3,10.1],[1.6,7.7,10.6]]
        for i in range(self.search_neighbor_num - 1):
            tmp_variable_list = []
            for j in range(self.variable_num - 1):
                tmp_variable_list.append(new_variable_list[j][i])
            cost_val_list.append(cost_function.Evaluate(tmp_variable_list))
            possible_val_list.append(tmp_variable_list)

        return possible_val_list[cost_val_list.index(min(cost_val_list))]
    
    def CreateVariableDict(self):
        super().CreateVariableDict(self)

    def CheckEndRequirements(self):
        #TBD
        return True

    def Solve(self):
        while ~self.CheckEndRequirements():
            # print(self.variable_list)
            # self.variable_list.Print()
            self.variable_list = self.UpdateVariables()
        #self.variable_list.Print() 
        return 


class SimulatedAnnealing(Algorithm):
    def __init__(self, variable_list, initIterator, initStepSize, initItBound, initItFunc, cost_function):
        super().__init__(variable_list, initIterator)

    def UpdateVariables(self):
        #TBD
        return self.variables

    def CreateVariableDict(self):
        super().CreateVariableDict(self)

    def CheckEndRequirements(self):
        #TBD
        return True

    def Solve(self):
        #TBD
        return


class ParticleSwarm(Algorithm):
    def __init__(self, variable_list, initIterator, initStepSize, initItBound, initItFunc, cost_function):
        super().__init__(variable_list, initIterator)

    def UpdateVariables(self):
        #TBD
        return self.variables

    def CreateVariableDict(self):
        super().CreateVariableDict(self)

    def CheckEndRequirements(self):
        #TBD
        return True

    def Solve(self):
        #TBD
        return

class GeneticEvo(Algorithm):
    def __init__(self, variable_list, initIterator, initStepSize, initItBound, initItFunc, cost_function):
        super().__init__(variable_list, initIterator)

    def UpdateVariables(self):
        #TBD
        return self.variables

    def CreateVariableDict(self):
        super().CreateVariableDict(self)

    def CheckEndRequirements(self):
        #TBD
        return True

    def Solve(self):
        #TBD
        return


def InitAlgorithm(name, variable_list, cost_function):
    if name == 'sa':
        return SimulatedAnnealing(variable_list, cost_function)
    elif name == 'ps':
        return ParticleSwarm(variable_list, cost_function)
    elif name == 'ge':
        return GeneticEvo(variable_list, cost_function)
    return SelfDefinedAlgorithm(variable_list, cost_function)