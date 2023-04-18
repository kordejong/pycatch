#!/usr/bin/env bash
set -e


pycatch_prefix="$LUE/../../kordejong/pycatch"
data_prefix="/scratch-shared/kor/pycatch/africa"


mkdir -p $data_prefix
cp ~/development/data/pycatch/africa/{elevation,flow_direction}.tiff $data_prefix
chmod 444 $data_prefix/{elevation,flow_direction}.tiff

# TODO test whether using uncompressed data is faster
# gdal_translate pathtoinput.tif pathforoutput.tif -co COMPRESS=NONE

cp \
    "$pycatch_prefix/inputs/rainfallFluxTwoCatchsJulAugSep0506.tss" \
    "$pycatch_prefix/inputs/airTemperatureArnaJulAugSep0506.tss" \
    "$pycatch_prefix/inputs/relativeHumidityArnasJulAugSep0506.tss" \
    "$pycatch_prefix/inputs/incomingShortwaveRadiationArnasJulAugSep0506.tss" \
    "$pycatch_prefix/inputs/windVelocityArnasJulAugSep0506.tss" \
    $data_prefix
chmod 444 $data_prefix/*.tss


# South-Africa
# nr_rows: 18000
# nr_cols: 26400
gdal_translate -projwin 14 -20 36 -35 elevation.tiff elevation-south_africa.tiff
gdal_translate -projwin 14 -20 36 -35 flow_direction.tiff flow_direction-south_africa.tiff




