### import lue.framework as lfr
### import pcraster as pcr

from osgeo import gdal


### def setclone(*args):
###     pcr.setclone(*args)
###
###
### def readmap(filename):
###     return lfr.from_gdal(filename, partition_shape)
###
###
### def report(array, filename):
###     lfr.to_gdal(array, filename)
###
###
### def boolean(arg):
###     if type(arg) == int or type(arg) == float:
###         if arg != 0:
###             return 1.0
###         else:
###             return 0.0
###     elif type(arg) == str:
###         return readmap(arg)
###     else:
###         raise NotImplementedError(arg)
###
###
### def nominal(arg):
###     if type(arg) == int:
###         return arg
###     elif type(arg) == str:
###         return readmap(arg)
###     else:
###         raise NotImplementedError(arg)
###
###
### def scalar(arg):
###     if type(arg) == lfr.PartitionedArray_float32_2:
###         return arg
###     elif type(arg) == int or type(arg) == float:
###         return float(arg)
###     elif type(arg) == str:
###         return readmap(arg)
###     else:
###         raise NotImplementedError(arg)
###
###
### def cover(arg1, arg2):
###     return lfr.where(lfr.valid(arg1), arg1, arg2)


### with open(timeseries_pathname) as timeseries_file:
###     lines = timeseries_file.readlines()
###     nr_rows_to_skip = int(lines[1]) + 2
###     lines = lines[nr_rows_to_skip:]
###     line = lines[timestep - 1]
###     values = line.split()[1:]

###     lookup_table = {}

###     for id_ in range(len(values)):
###         lookup_table[id_] = values[id_]


import os
import numpy as np
import psutil
from psutil._common import bytes2human


def memory_usage(process_id=os.getpid()):
    process = psutil.Process(process_id)
    # rss
    # memory = process.memory_info()[0] / (1024**3)
    return bytes2human(process.memory_info()[0])


def load(name):

    assert name in ["lue", "pcraster"]

    if name == "lue":

        import lue.framework as lfr
        import lue.pcraster as pcr
        import lue.pcraster.framework as pcrfw

        @lfr.runtime_scope
        def create_and_run_model(function, *args):
            function(*args)

        pcr.run_model = create_and_run_model

        def set_clone(pathname):
            raster_dataset = gdal.Open(pathname)

            array_shape = raster_dataset.RasterYSize, raster_dataset.RasterXSize
            partition_shape = (300, 300)  # TODO

            geo_transform = raster_dataset.GetGeoTransform()
            cell_shape = geo_transform[1], -geo_transform[5]
            assert cell_shape[0] == cell_shape[1]
            cell_size = cell_shape[0]

            pcr.configuration.array_shape = array_shape
            pcr.configuration.partition_shape = partition_shape
            pcr.configuration.cell_size = cell_size

        pcr.setclone = set_clone

        def print_max(name, raster):
            print(f"{name}: {pcr.mapmaximum(raster).get()}")

        def timeinputscalar(timeseries_pathname: str, id_expression, timestep: int):
            lines = open(timeseries_pathname).readlines()
            nr_rows_to_skip = int(lines[1]) + 2
            lines = lines[nr_rows_to_skip:]
            line = lines[timestep - 1]
            values = line.split()[1:]
            lookup_table = {id_ + 1: float(values[id_]) for id_ in range(len(values))}

            return lfr.reclassify(id_expression, lookup_table, dtype=np.float32)

        pcr.timeinputscalar = timeinputscalar

        pcr.memory_usage = memory_usage

        pcr.print_max = print_max

        # framework = lfr
        # framework.setclone = setclone
        # framework.boolean = boolean
        # framework.nominal = nominal
        # framework.scalar = scalar
        # framework.cover = cover
        # framework.readmap = readmap
        # framework.report = report

    elif name == "pcraster":
        # framework = pcr
        import pcraster as pcr
        import pcraster.framework as pcrfw

    return pcr, pcrfw
