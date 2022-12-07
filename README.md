# EE581_Project F22
Omar Radwan & Yilin Zhang


1. Relevant Files

There are a number of example parameter instantiations within the ./data from this top level directory
1. comp_arch_ex.json     - Computer Architecture Example as outlined in report
2. fpga_synth_setup.json int_test.json - FPGA synthesis example as outlined in report
3. sample_from_luca.json - initial example file that we worked on with Luca and modified a little to initially test things out


2. Project Data
In the scripts folder there is a number of scripts and directories, and those contain the scripts used to find the uniform, linear, and square distance weighted random sampling, and this data is used in the report


3. To run

Must have the following libraries copy,math,time,numpy,ateval,functools,sympy,random,os,json,argparse

To run, please run the following using Python3.8+ and the libraries listed above

python3 ./src/parser.py -p ./data/fpga_synth_setup.json # can use other files with -p
