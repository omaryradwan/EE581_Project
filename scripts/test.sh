for i in {1..10}; do
    echo $i
    ./run.sh > fpga_instance_run_${i}.txt
    python3 parser.py -p ../data/comp_arch_ex.json > arch_instance_run_${i}.txt
done
