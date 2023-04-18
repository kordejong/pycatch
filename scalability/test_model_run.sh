#!/usr/bin/env bash
set -e

pycatch_prefix="$LUE/../../kordejong/pycatch"
lue_qa_data_prefix="$LUE/../../../../data/lue_qa"

export PYTHONPATH="$pycatch_prefix:$pycatch_prefix/pcrasterModules:$LUE_OBJECTS/lib/python3.10:$PYTHONPATH"
export LD_PRELOAD=$EBROOTGPERFTOOLS/lib/libtcmalloc_minimal.so.4

$pycatch_prefix/scalability/pycatch.py \
    --mca pml ucx --mca btl ^uct \
    --hpx:threads="16" \
    --hpx:print-bind \
    --lue:count="1" \
    --lue:nr_workers="1" \
    --lue:array_shape="[6000, 9600]" \
    --lue:partition_shape="[1500, 1500]" \
    --lue:result="$lue_qa_data_prefix/snellius/pycatch.py/cluster_node/strong_scalability/1.json"
