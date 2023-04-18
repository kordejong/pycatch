#!/usr/bin/env bash
set -e


pycatch_prefix="$LUE/../../kordejong/pycatch"

export PYTHONPATH="$pycatch_prefix:$pycatch_prefix/pcrasterModules:$LUE_OBJECTS/lib/python3.10:$PYTHONPATH"
export LD_PRELOAD=$EBROOTGPERFTOOLS/lib/libtcmalloc_minimal.so.4

nr_nodes=1
nr_tasks=8  # $nr_nodes * 8 numa_nodes
array_shape="18000, 26400"


mkdir -p /home/kor/development/data/lue_qa/snellius/pycatch.py/cluster_node/strong_scalability
sbatch --job-name strong_scalability-pycatch.py-$nr_nodes --exclusive --export=ALL << END_OF_SLURM_SCRIPT
#!/usr/bin/env bash
#SBATCH --nodes=$nr_nodes
#SBATCH --ntasks=$nr_tasks
#SBATCH --cpus-per-task=16
#SBATCH --output=/home/kor/development/data/lue_qa/snellius/pycatch.py/cluster_node/strong_scalability/$nr_nodes.out
#SBATCH --partition=thin
#SBATCH --exclusive
#SBATCH --export=ALL
#SBATCH --time=60


mpirun --verbose --display-map --display-allocation --mca pml ucx --mca btl ^uct --n $nr_tasks pycatch.py --hpx:threads="16" --hpx:print-bind --lue:count="1" --lue:nr_workers="$nr_nodes" --lue:array_shape="[$array_shape]" --lue:partition_shape="[2000, 2000]" --lue:result="/home/kor/development/data/lue_qa/snellius/pycatch.py/cluster_node/strong_scalability/$nr_nodes.json" 
END_OF_SLURM_SCRIPT
