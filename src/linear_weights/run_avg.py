
from math import *
fpga_f = open("csv_fpga_results.txt")
arch_f = open("csv_arch_results.txt")

for i in fpga_f.readlines():
    i = i.rstrip('\n')
    # print(i)
    fpga_l = i.split(',')
    fpga_l = list(filter(None, fpga_l))
    fpga_l = list(filter(bool, fpga_l))
    fpga_l = list(filter(len, fpga_l))
    fpga_l = list(filter(lambda item: item, fpga_l))
    int_fpga_l = [int(x) for x in fpga_l]
    print("avg", sum(int_fpga_l)/len(int_fpga_l))
