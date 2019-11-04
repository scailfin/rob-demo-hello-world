# This file is part of the Reproducible Open Benchmarks for Data Analysis
# Platform (ROB).
#
# Copyright (C) 2019 NYU.
#
# ROB is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""This is an adopted version of the REANA-Demo-HelloWorld demo. The main
intend of this application is to demonstrate ROB and for testing the multi-
process backend.
"""

from __future__ import absolute_import, print_function

import argparse
import errno
import os
import sys
import time


def hello(inputfile, outputfile, greeting='Hello', sleeptime=0.0):
    """Write greeting for every name in a given input file to the output file.
    The optional waiting period delays the output between each input name.

    Parameters
    ----------
    inputfile: file
        Text file containing one name per line
    outputfile: file
        Text file that will contain a greeting for each name in the input file
        per output line
    greeting: string
        The greeting phrase
    sleeptime: float
        Wait period after each line that is written to the output file
    """
    # Read names to greet. Only consider names that are not empty.
    names = []
    with open(inputfile, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line != '':
                names.append(line)

    # Ensure output directory exists:
    # influenced by http://stackoverflow.com/a/12517490
    out_dir = os.path.dirname(outputfile)
    if out_dir != '':
        if not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

    # Write greetings to output file and sleep in between. If the greeting
    # phrase is empty no output will be writtent to the file but the output
    # file will still be created.
    with open(outputfile, 'w') as f:
        if len(greeting) > 0:
            for name in names:
                f.write(greeting + ' ' + name + '\n')
                f.flush()
                time.sleep(sleeptime)


if __name__ == '__main__':
    args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", required=True)
    parser.add_argument("-o", "--outputfile", required=True)
    parser.add_argument("-g", "--greeting", default='Hello', required=False)
    parser.add_argument("-s", "--sleeptime", default=1.0, type=float, required=False)

    parsed_args = parser.parse_args(args)

    hello(
        inputfile=parsed_args.inputfile,
        outputfile=parsed_args.outputfile,
        greeting=parsed_args.greeting,
        sleeptime=parsed_args.sleeptime
    )
