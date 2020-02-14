"""Post-processing code for hello workd Demo. This code is included with
flowServ for testing purposes only.
"""

from __future__ import absolute_import, division, print_function

import argparse
import errno
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import sys
import time

from flowserv.service.postproc.client import Runs


def main(rundir, outputfile):
    """Write greeting for every name in a given input file to the output file.
    The optional waiting period delays the output between each input name.

    """
    # Count frequency of n-grams for each run
    keys = set()
    results = list()
    for run in Runs(rundir):
        # Get five most frequent n-grams
        ngrams = dict()
        with open(run.get_file('results/greetings.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) >= 3:
                    for i in range(len(line) - 2):
                        ng = line[i:i+3]
                        ngrams[ng] = ngrams.get(ng, 0) + 1
        candidates = [(n, ngrams[n]) for n in ngrams]
        candidates.sort(key=lambda p:p[1], reverse=True)
        if len(candidates)> 5:
            candidates = candidates[:5]
        results.append((run.name, candidates))
        # Add n-grams to global set of result keys
        for c in candidates:
            keys.add(c[0])
        # Delay execution to allow for testing running post-processing
        # workflows
        time.sleep(10)
    keys = sorted(list(keys))
    # Write plot output file. Ensure that output directory exists:
    # influenced by http://stackoverflow.com/a/12517490
    if not os.path.exists(os.path.dirname(outputfile)):
        try:
            os.makedirs(os.path.dirname(outputfile))
        except OSError as exc:  # guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    # create plot
    fig, ax = plt.subplots()
    n_groups = len(keys)
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    series = 0
    for name, candidates in results:
        ngrams = dict()
        for key, count in candidates:
            ngrams[key] = count
        values = list()
        for key in keys:
            values.append(ngrams.get(key, 0))
        plt.bar(
            index,
            values,
            bar_width,
            alpha=opacity,
            color=colors[series % len(colors)],
            label=name
        )
        index = index + bar_width
        series += 1
    plt.xlabel('3-grams')
    plt.ylabel('Counts')
    plt.xticks(index, keys)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outputfile)


if __name__ == '__main__':
    args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--runs", required=True)
    parser.add_argument("-o", "--outputfile", required=True)

    parsed_args = parser.parse_args(args)

    main(rundir=parsed_args.runs, outputfile=parsed_args.outputfile)
