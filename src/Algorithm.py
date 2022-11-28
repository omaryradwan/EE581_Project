# This file defines the Algorithm Class. This class is the parent class of detailed algorithm classes.
#
# All the algorithms should contain the following attributes:
#       variable_list       --          This is a list of variable class                eg: [v1, v2, v3]
#       iterating_parameter --          The iterating parameter                         eg: time
#       cost_function       --          Then cost function of variables                 eg: x^2+y^2
#       variable_num        --          The number of variables                         eg: 3
#       search_neighbor_num --          The number of neighbors to check                eg: 10
#
# The algorithm should contain the following functions:
#       CreateVariableDict  --          Randomly slelect neighbor of initial point to create initial dict, each variable n points.
import EvalSpace
import copy

class Algorithm:
    def __init__(self, variable_list, cost_function, iterating_parameter, assertions):
        self.variable_list = variable_list
        self.iterating_parameter = iterating_parameter
        self.cost_function = cost_function
        self.variable_num = len(variable_list)
        self.search_neighbor_num = 100   # TO DO: Set the number 10 to a parameter in __init__
        self.assertions = EvalSpace.VerifyAssertions(assertions, iterating_parameter, variable_list)
        # local_var_list = variable_list
        self.name = ''


    def UpdateVariables(self):
        pass

    def CreateVariableDict(self):
        pass

    def CheckEndRequirements(self):
        pass

    def Solve(self):
        pass


class SelfDefinedAlgorithm(Algorithm):
    def __init__(self, variable_list, cost_function, iterating_parameter, assertions):
        super().__init__(variable_list, cost_function, iterating_parameter, assertions)
        self.name = 'Self Defined Algorithm'

    def CreateVariableListList(self):
        new_variable_list_list = []
        for i in range(self.variable_num):
            tmp_variable = self.variable_list[i]
            tmp_new_list = tmp_variable.GenRandomNeighbors(self.search_neighbor_num, self.assertions, self.iterating_parameter, self.variable_list)
            new_variable_list_list.append(tmp_new_list)
        return new_variable_list_list

    def GetLocalOptimalValListsWildly(self):
        new_variable_list_list = self.CreateVariableListList() #[[1,1.4,1.6],[7,7.3,7.7],[10,10.1,10.6]]
        cost_val_list = []
        possible_val_list = [] #[[1,7,10],[1.4,7.3,10.1],[1.6,7.7,10.6]]

        cost_val_list.append(self.cost_function.get_cost())
        possible_val_list.append(self.variable_list)

        for i in range(self.search_neighbor_num - 1):
            tmp_variable_list = []
            for j in range(self.variable_num):
                tmp_variable_list.append(new_variable_list_list[j][i])
            # print(tmp_variable_list)
            self.cost_function.construct_parameter_space(self.iterating_parameter, tmp_variable_list)
            cost_val_list.append(self.cost_function.get_cost())
            possible_val_list.append(tmp_variable_list)
        self.variable_list = possible_val_list[cost_val_list.index(min(cost_val_list))]
        # print("Local Cost List is: ", cost_val_list)
        print("Local Optimal Cost is: ", cost_val_list[cost_val_list.index(min(cost_val_list))])
        self.variable_list = possible_val_list[cost_val_list.index(min(cost_val_list))]
        for i in range(self.variable_num):
            if self.variable_list[i].type == 'composite':
                for children in self.variable_list[i].children_list:
                    for child in children:
                        print(child.name, ": ", child.temporary_val)
            else:
                print(self.variable_list[i].name, ": ", self.variable_list[i].temporary_val)

    def CoordinateRandomSearch(self, i):
        tmp_list_list = []
        tmp_variable = self.variable_list[i]
        tmp_variable_list = tmp_variable.GenRandomNeighbors(self.search_neighbor_num, self.assertions, self.iterating_parameter, self.variable_list)
        for j in range(len(tmp_variable_list)):
            tmp_new_variable = tmp_variable_list[j]
            tmp_variable_list_copy = copy.deepcopy(self.variable_list)
            tmp_variable_list_copy[i] = tmp_new_variable
            tmp_list_list.append(tmp_variable_list_copy)
        return tmp_list_list

    def GetLocalOptimalValListsCoordinately(self):
        total_possible_list_list = []
        total_cost_list = []
        total_cost_list.append(self.cost_function.get_cost())
        total_possible_list_list.append(self.variable_list)
        for i in range(self.variable_num):
            tmp_list_list = self.CoordinateRandomSearch(i)
            for j in range(len(tmp_list_list)):
                self.cost_function.construct_parameter_space(self.iterating_parameter, tmp_list_list[j])
                total_cost_list.append(self.cost_function.get_cost())
                total_possible_list_list.append(tmp_list_list[j])
        print("Local Optimal Cost is: ", min(total_cost_list))
        # print(min(total_cost_list))
        # print(total_cost_list)
        # print(total_possible_list_list)
        self.variable_list = total_possible_list_list[total_cost_list.index(min(total_cost_list))]
        for i in range(self.variable_num):
            if self.variable_list[i].type == 'composite':
                for children in self.variable_list[i].children_list:
                    for child in children:
                        print(child.name, ": ", child.temporary_val)
            else:
                print(self.variable_list[i].name, ": ", self.variable_list[i].temporary_val)


    def CheckEndRequirements(self):
        return self.iterating_parameter.IsOverBound()

    def Solve(self):
        iteration_number = 0
        while not self.CheckEndRequirements():
            print('\nIteration number: {:2} Iterating Parameter Value: {:2} Bound: {:2} Finishing Percentage: {:2.2%}'.format(iteration_number, self.iterating_parameter.temporary_val,
                    self.iterating_parameter.bound,self.iterating_parameter.temporary_val/self.iterating_parameter.bound))
            iteration_number += 1
            self.iterating_parameter.Iterate()
            self.GetLocalOptimalValListsWildly()
            self.cost_function.construct_parameter_space(self.iterating_parameter, self.variable_list)
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


def InitAlgorithm(name, variable_list, cost_function, iterating_parameter, assertions):


    if name == 'sa':
        return SimulatedAnnealing(variable_list, cost_function, iterating_parameter, assertions)
    elif name == 'ps':
        return ParticleSwarm(variable_list, cost_function, iterating_parameter, assertions)
    elif name == 'ge':
        return GeneticEvo(variable_list, cost_function, iterating_parameter, assertions)
    return SelfDefinedAlgorithm(variable_list, cost_function, iterating_parameter, assertions)
