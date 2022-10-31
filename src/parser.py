import json
import parameter_types
import argparse
import os
# import Algorithm


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', "--parameter_file", type=str, required=True)

    args = parser.parse_args();

    if not os.path.exists(args.parameter_file):
        print("Error: " + args.parameter_file + " does not exist, exiting")
        return -1

    parameter_file = open(args.parameter_file, 'r')
    # parameter_file_contents = parameter_file.read()

    parameter_object_list = []
    json_params = json.load(parameter_file)
    for para_declaration in json_params:
        if para_declaration["type"] not in parameter_types.parameter_types.keys():
            print("JSON file invalid " + para_declaration["type"]+ " is not a valid type")
            return -1
        tmp_object = parameter_types.InitTypedVariable(para_declaration)
        parameter_object_list.append(tmp_object)

    # print(parameter_object_list)
    # solve_algorithm = Algorithm(parameter_object_list, initIterator, initStepSize, initItBound, initItFunc, cost_function)
    # local_optimal_list = solve_algorithm.Solve()
    # print(local_optimal_list)


if __name__ == "__main__":
    main()
