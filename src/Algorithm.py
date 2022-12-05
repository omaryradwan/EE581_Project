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
import math
import time
import numpy as np
time_start = time.time()
end_time = time.time()
class Algorithm:
    def __init__(self, variable_list, cost_function, iterating_parameter, assertions):
        self.variable_list = variable_list
        self.iterating_parameter = iterating_parameter
        self.cost_function = cost_function
        self.variable_num = len(variable_list)
        self.min_cost = math.inf
        self.search_neighbor_num = 10   # TO DO: Set the number 10 to a parameter in __init__
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
            if self.cost_function.get_cost() == 0:
                continue
            cost_val_list.append(self.cost_function.get_cost())
            possible_val_list.append(tmp_variable_list)

        for i in cost_val_list:
            if i == 0:
                cost_val_list.remove(i)
        # print(cost_val_list)
        self.variable_list = possible_val_list[cost_val_list.index(min(cost_val_list))]
        # print("Local Cost List is: ", cost_val_list)

        print("Local Optimal Cost is: ", cost_val_list[cost_val_list.index(min(cost_val_list))])
        if self.min_cost > cost_val_list[cost_val_list.index(min(cost_val_list))]:
            self.min_cost = cost_val_list[cost_val_list.index(min(cost_val_list))]
        self.variable_list = possible_val_list[cost_val_list.index(min(cost_val_list))]

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

    def CheckEndRequirements(self):
        return self.iterating_parameter.IsOverBound()



    nums = set();
    def solve2(self):
        iteration_num = 0;
        initial_half_list = []
        for i in range(self.variable_num):
            tmp_param_list = self.variable_list[i]
            initial_parameter_half_list = tmp_param_list.GenRandomNeighbors(self.search_neighbor_num,self.assertions,self.iterating_parameter,self.variable_list)
            initial_half_list.append(initial_parameter_half_list)

        half_list = copy.deepcopy(initial_half_list)
        while not self.CheckEndRequirements():
            iteration_num += 1;
            self.iterating_parameter.Iterate()
            print('\nIteration number: {:2} Iterating Parameter Value: {:2} Bound: {:2} Finishing Percentage: {:2.2%}'.format(iteration_num, self.iterating_parameter.temporary_val, self.iterating_parameter.bound,self.iterating_parameter.temporary_val/self.iterating_parameter.bound))
            full_list = []
            print('\nIteration number: {:2} Iterating Parameter Value: {:2} Bound: {:2} Finishing Percentage: {:2.2%}'.format(iteration_num, self.iterating_parameter.temporary_val, self.iterating_parameter.bound,self.iterating_parameter.temporary_val/self.iterating_parameter.bound))
            time_start = time.time();

            loop_half_list = copy.deepcopy(half_list)
            for i in range(len(loop_half_list)):
                for j in range(len(loop_half_list[i])):
                    tmp_var = loop_half_list[i][j].GenRandomNeighbors(1,self.assertions,self.iterating_parameter, self.variable_list)
                    loop_half_list[i].extend(tmp_var)
                full_list.append(loop_half_list[i])


            cost_list = []
            for i in range(2*self.search_neighbor_num):
                tmp_conjoined_param_list = []
                for j in range(self.variable_num):
                    tmp_conjoined_param_list.append(full_list[j][i])
                    self.cost_function.construct_parameter_space(self.iterating_parameter, tmp_conjoined_param_list)
                cost_inst = self.cost_function.get_cost()
                if cost_inst == 0:
                    cost_inst = math.inf
                cost_list.append(cost_inst)

            # print("FULL COST LIST", cost_list)
            # print("SORTED COST LIST " , sorted(cost_list))
            # print("/// Runtime: ", time.time() - time_start)


            best_cost_index = cost_list.index(min(cost_list))
            # print("BEST COST INDEX ", best_cost_index)
            optimal_param_list = list()
            for i in range(self.variable_num):
                optimal_param_list.append(full_list[i][best_cost_index])

            self.variable_list = copy.deepcopy(optimal_param_list)
            self.cost_function.construct_parameter_space(self.iterating_parameter, self.variable_list)
            print("######BEST LOCAL Cost is ", self.cost_function.get_cost())
            for i in range(self.variable_num):
                if self.variable_list[i].type == 'composite':
                    for children in self.variable_list[i].children_list:
                        for child in children:

                            print("#####", child.name, ":", child.temporary_val)
                else:
                    print("#####", self.variable_list[i].name, ":", self.variable_list[i].temporary_val)


            indx_size = int(len(cost_list)/2)
            lowest_cost_indices = sorted(range(len(cost_list)), key = lambda sub: cost_list[sub])[:indx_size]
            print(lowest_cost_indices)
            new_half = []

            for i in range(self.variable_num):
                tmp_list = []
                for j in lowest_cost_indices:
                    tmp_list.append(full_list[i][j])
                new_half.append(tmp_list)


            # fake_full_list = copy.deepcopy(full_list)
            # for i in range(int(len(full_list)/2)):
            #     min_in_fake_full_list_index = (cost_list.index(max(cost_list)))
            #     for j in range(self.variable_num):
            #         del fake_full_list[j][min_in_fake_full_list_index]
            #     del cost_list[min_in_fake_full_list_index]
            half_list = copy.deepcopy(new_half)

            # cost_list = []
            # for i in range(self.search_neighbor_num):
            #     tmp_conjoined_param_list = []
            #     for j in range(self.variable_num):
            #         tmp_conjoined_param_list.append(new_half[j][i])
            #         self.cost_function.construct_parameter_space(self.iterating_parameter, tmp_conjoined_param_list)
            #     cost_inst = self.cost_function.get_cost()
            #     if cost_inst == 0:
            #         cost_inst = math.inf
            #     self.nums.add(cost_inst)
            #     cost_list.append(cost_inst)

            # print("FAKE SORTED FULL COST LIST", cost_list)
            # print("FAKE SORTED FULL COST LIST", sorted(cost_list))
            # print("Cost nums size", len(self.nums))


            # new_half = copy.deepcopy(fake_full_list)
            # half_list = copy.deepcopy(new_half)

        self.min_cost = self.cost_function.get_cost()

        return



    def Solve(self):
        iteration_number = 0
        half_list = []
        for i in range(self.variable_num):
            tmp_variable = self.variable_list[i]
            init_val_list = tmp_variable.GenRandomNeighbors(self.search_neighbor_num, self.assertions, self.iterating_parameter, self.variable_list)
            half_list.append(init_val_list)

        while not self.CheckEndRequirements():
            print('\nIteration number: {:2} Iterating Parameter Value: {:2} Bound: {:2} Finishing Percentage: {:2.2%}'.format(iteration_number, self.iterating_parameter.temporary_val, self.iterating_parameter.bound,self.iterating_parameter.temporary_val/self.iterating_parameter.bound))

            iteration_number += 1
            time_start = time.time()
            full_list = []

            for i in range(len(half_list)):
                for j in range(len(half_list[i])):
                    tmp_variable = half_list[i][j]
                    new_tmp_variable_list = tmp_variable.GenRandomNeighbors(1, self.assertions, self.iterating_parameter, self.variable_list)
                    half_list[i].extend(new_tmp_variable_list)


                full_list.append(half_list[i])

            cost_full_list = []

            for i in range(2*self.search_neighbor_num):
                tmp_variable_list = [] #[Int1, Bool1, Com1]
                for j in range(self.variable_num):
                    tmp_variable_list.append(full_list[j][i])

                self.cost_function.construct_parameter_space(self.iterating_parameter, tmp_variable_list)
                cost_val = self.cost_function.get_cost()
                if cost_val == 0:
                    cost_val = math.inf
                cost_full_list.append(cost_val)
            print("FULL COST LIST: ", cost_full_list)

            minimum_index = cost_full_list.index(min(cost_full_list))

            new_half_list_index = list(np.argpartition(np.array(cost_full_list), self.search_neighbor_num))
            nxt_half_list = []
            nxt_self_list = []
            for i in range(self.variable_num):
                tmp_half_list = []
                for j in new_half_list_index:
                    tmp_half_list.append(full_list[i][j])
                nxt_self_list.append(full_list[i][minimum_index])
                nxt_half_list.append(tmp_half_list)
            half_list = copy.deepcopy(nxt_half_list)


            self.variable_list = copy.deepcopy(nxt_self_list)
            print("/// Runtime: ", time.time() - time_start)
            self.cost_function.construct_parameter_space(self.iterating_parameter, self.variable_list)
            print("######BEST LOCAL Cost is ", self.cost_function.get_cost())
            for i in range(self.variable_num):
                if self.variable_list[i].type == 'composite':
                    for children in self.variable_list[i].children_list:
                        for child in children:

                            print("#####", child.name, ":", child.temporary_val)
                else:
                    print("#####", self.variable_list[i].name, ":", self.variable_list[i].temporary_val)

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
