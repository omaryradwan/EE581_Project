import os
import json
import argparse
import Algorithm
import CostFunction
import parameter_types


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', "--parameter_file", type=str, required=True)
    parser.add_argument('-a', "--algorithm_selection", type=str,
    help = 'Select one of algorithm in [se, ps, eo]. If not selected, default value is self defined algorithm.')
    
    args = parser.parse_args();

    if not os.path.exists(args.parameter_file):
        print("Error: " + args.parameter_file + " does not exist, exiting")
        return -1

    parameter_file = open(args.parameter_file, 'r')
    # parameter_file_contents = parameter_file.read()

    parameter_object_list = []
    parameter_check_map = {}
    json_params = json.load(parameter_file)

    print("Parameter Loading...")
    for para_declaration in json_params:
        if para_declaration == 'cost_function':
            continue
        # print(para_declaration)
        # print(json_params[para_declaration])
        para_json = json_params[para_declaration]
        if para_json['type'] not in parameter_types.parameter_types.keys():
            print("JSON file invalid " + para_json['type']+ " is not a valid type")
            return -1
        tmp_object = parameter_types.InitTypedVariable(para_json)
        parameter_check_map[para_json['name']] = para_json['type']
        parameter_object_list.append(tmp_object)
    print("Parameter Loaded Successfully\nAll Loaded Parameters are:")
    print(parameter_check_map)

    print("Cost Function Loading...")    
    cost_function_json = json_params['cost_function']
    cost_function = CostFunction.CostFunction(cost_function_json['formula'])
    print("Cost Function Loaded Successfully\nCost Function is:")
    print(cost_function.formula)

    print("Algorithm Initializing...")
    solve_algorithm = Algorithm.InitAlgorithm(args.algorithm_selection, parameter_object_list, cost_function)
    print("Algorithm Initialized\n"+solve_algorithm.name + " Selected")

    print("Algorithm Starts...")
    # solve_algorithm.Solve()
    print("Algorithm Ends")

if __name__ == "__main__":
    main()
