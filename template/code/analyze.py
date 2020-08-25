# This file is part of the Reproducible Open Benchmarks for Data Analysis
# Platform (ROB).
#
# Copyright (C) 2019 NYU.
#
# ROB is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Analytics code for the adopted hello workd Demo. Reads a text file (as
produced by the helloworld.py code) and outputs the number of distinct 3-grams,
number of lines, and the overall score (#3-grams/#lines).
"""

from __future__ import absolute_import, division, print_function

import argparse
import errno
import os
import json
import sys


def main(inputfile, outputfile):
    """Read input file lines. For each non-empty line the distinct 3-grams are
    added to the overall 3-gram index. The output is a Json object that
    contains the total number of 3-grams, number of lines and the score.

    Parameters
    ----------
    inputfile: file
        Text file containing greeting lines
    outputfile: file
        Output file that will contain he result in Json format
    """
    # Create set of distinct 3-grams. Keep track of number of lines.
    ngrams = set()
    line_count = 0
    with open(inputfile, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) >= 3:
                for i in range(len(line) - 2):
                    ngrams.add(line[i:i + 3])
                line_count += 1
    # Create results object
    if len(ngrams) > 0 and line_count > 0:
        score = len(ngrams) / line_count
    else:
        score = 0.0
    results = {
        'ngrams': len(ngrams),
        'linecount': line_count,
        'score': score
    }
    # Write analytics results. Ensure that output directory exists:
    # influenced by http://stackoverflow.com/a/12517490
    out_dir = os.path.dirname(outputfile)
    if out_dir != '':
        if not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
    with open(outputfile, 'w') as f:
        json.dump(results, f)


if __name__ == '__main__':
    args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", required=True)
    parser.add_argument("-o", "--outputfile", required=True)

    parsed_args = parser.parse_args(args)

    main(inputfile=parsed_args.inputfile, outputfile=parsed_args.outputfile)
