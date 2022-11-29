import os
import json
import argparse
import Algorithm
import EvalSpace
import parameter_types

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', "--parameter_file", type=str, required=True)
    parser.add_argument('-a', "--algorithm_selection", type=str,
    help = 'Select one of algorithm in [se, ps, eo]. If not selected, default value is self defined algorithm.')

    args = parser.parse_args()

    if not os.path.exists(args.parameter_file):
        print("Error: " + args.parameter_file + " does not exist, exiting")
        return -1

    parameter_file = open(args.parameter_file, 'r')
    # parameter_file_contents = parameter_file.read()

    parameter_object_list = []
    parameter_check_map = {}
    json_params = json.load(parameter_file)

    print("Typed Parameter Loading...")
    for para_declaration in json_params:
        if para_declaration == 'iterating_variable':
            break
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

    print("Iterating Parameter Loading...")
    iterating_parameter_json = json_params['iterating_variable']
    iterating_parameter = parameter_types.InitIteratingVariable(iterating_parameter_json)
    print("Iterating Parameter Loaded Successfylly")

    print("Cost Function Loading...")
    cost_function_json = json_params['cost_function']

    print("Assertions Loading...")
    assertions_json = json_params['assertions']
    assertions = parameter_types.InitAssertions(assertions_json)
    print("Cost Function and Assertions Loaded Successfully")

    print("Creating instance parameter computation environment")

    cost_function = EvalSpace.EvalCost(cost_function_json['formula'], iterating_parameter, parameter_object_list)
    print("Populating parameter dictionary for assertion and cost function resolution")
    print("Running cost function")
    inst_cost = cost_function.get_cost()
    print("Total cost of initial state is", inst_cost)

    print("Verifying assertions")
    check_assertions = EvalSpace.VerifyAssertions(assertions, iterating_parameter, parameter_object_list)
    is_assert_list_valid = check_assertions.verify_assertions()

    print("Algorithm Initializing...")

    solve_algorithm = Algorithm.InitAlgorithm(args.algorithm_selection, parameter_object_list, cost_function, iterating_parameter, assertions)

    print("Algorithm Initialized\n"+solve_algorithm.name + " Selected")

    print("Algorithm Starts...")
    solve_algorithm.Solve()
    print("Algorithm Ends")
    final_best_parameter_list = solve_algorithm.variable_list


if __name__ == "__main__":
    main()
