#!/usr/bin/env bash
set -e


data_prefix="/scratch-shared/kor/pycatch/africa"

mkdir -p $data_prefix
cp ~/development/data/pycatch/africa/{elevation,flow_direction}.tiff $data_prefix

# TODO test whether using uncompressed data is faster
# gdal_translate pathtoinput.tif pathforoutput.tif -co COMPRESS=NONE
