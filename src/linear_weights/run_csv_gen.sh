rm -rf fpga_results.txt arch_results.txt
range=`wc -l < numbers_only_arch_instance_run_1.txt`
for (( i=1; i<=$range; i++)) do
    fpga_list=""
    arch_list=""
    for j in `ls numbers_only_arch*`; do
        arch_list+=`sed "${i}d" $j`
        arch_list+=","
    done
    echo $arch_list >> arch_results.txt

    for j in `ls numbers_only_fpga*`; do
        fpga_list+=`sed "${i}d" $j`
        fpga_list+=","
    done
    echo $fpga_list >> fpga_results.txt

done

    cat fpga_results.txt | sed 's# #,#g' > csv_fpga_results.txt
    cat arch_results.txt | sed 's# #,#g' > csv_arch_results.txt
