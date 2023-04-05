#!/usr/bin/env python
from main import pycatch as main_pycatch
import lue.framework as lfr
import lue.qa as lqa
import docopt
import ast
import os.path
import sys


# @lfr.runtime_scope
def pycatch(
        nr_workers,
        count,
        array_shape,
        partition_shape,
        result_pathname,
    ):

    # Given the information passed in, run pycatch, and report the amount of time
    # this took.

    experiment = lqa.ArrayExperiment(nr_workers, array_shape, partition_shape)
    experiment.start()

    for c in range(count):
        # Perform some calculations on the workers and keep track of the timings

        run = lqa.Run()

        run.start()

        # We assume here that this function blocks until done. This is true if LUE's
        # scope_runtime decorator is used.
        main_pycatch(partition_shape)

        run.stop()

        experiment.add(run)

    experiment.stop()
    lqa.save_results(experiment, result_pathname)


def parse_count(string):

    return int(string)


def parse_shape(string):

    literal = ast.literal_eval(string)
    assert isinstance(literal, list), literal
    assert all([isinstance(element, int) for element in literal]), literal
    assert len(literal) == 2, literal

    return tuple(literal)


def main():
    lue_usage = """\
Dummy script for scalability experiments

Usage:
    {command} --lue:count=<count> --lue:nr_workers=<nr_workers>
        --lue:array_shape=<shape> --lue:partition_shape=<shape>
        --lue:result=<result>

Options:
    --lue:count=<count>             Number of times to repeat the experiment
    --lue:nr_workers=<nr_workers>   Number of workers used in experiment
    --lue:array_shape=<shape>       Shape of array: nr_rows,nr_cols
    --lue::partition_shape=<shape>  Shape of partition: nr_rows,nr_cols
    --lue::result=<result>          Pathname of file to write results in
""".format(
        command=os.path.basename(sys.argv[0]))

    # Filter out arguments meant for the HPX runtime. These are automatically parsed by the
    # code that starts the runtime.
    hpx_arguments = [arg for arg in sys.argv[1:] if arg.startswith("--hpx:")]

    # Parse arguments which are passed in by the LUE QA generated script
    lue_arguments = [arg for arg in sys.argv[1:] if arg.startswith("--lue:")]
    lue_arguments = docopt.docopt(lue_usage, lue_arguments)
    nr_workers = parse_count(lue_arguments["--lue:nr_workers"])
    count = parse_count(lue_arguments["--lue:count"])
    array_shape = parse_shape(lue_arguments["--lue:array_shape"])
    partition_shape = parse_shape(lue_arguments["--lue:partition_shape"])
    result_pathname = lue_arguments["--lue:result"]

    # arguments = [arg for arg in sys.argv[1:] if not arg in hpx_arguments and not arg in lue_arguments]
    # TODO Parse any remaining arguments if necessary

    pycatch(nr_workers, count, array_shape, partition_shape, result_pathname)


if __name__ == "__main__":
    main()
