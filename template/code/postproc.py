from collections import Counter

import argparse
import errno
import matplotlib.pyplot as plt
import os
import sys
import time

from flowserv.service.postproc.client import Runs


def main(rundir, outputfile=None):
    """Create a plot showing the frequency of the 25 most frequent n-grams in
    the greeting files of all runs. Counts only those n-grams that do not contain
    a whitespace character.
    """
    # Count frequency of n-grams for all runs.
    ngrams = Counter()
    for run in Runs(rundir):
        with open(run.get_file('results/greetings.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) >= 3:
                    for i in range(len(line) - 2):
                        ng = line[i:i + 3].upper()
                        if not ' ' in ng:
                            ngrams[ng] += 1
        # Delay execution to allow for testing running post-processing
        # workflows
        time.sleep(0)
    # Create plot
    x = list()
    y = list()
    for ngram, count in ngrams.most_common(25):
        x.append(ngram)
        y.append(count)
    x = x[::-1]
    y = y[::-1]
    plt.style.use('ggplot')
    x_pos = [i for i, _ in enumerate(x)]
    plt.figure(figsize=(10, 15))
    plt.barh(x_pos, y, color='green')
    plt.xlabel("Count")
    plt.title("Top-25 n-grams by frequency")
    plt.yticks(x_pos, x)
    # Write to file if output directory is given. Otherwise
    # show the plot.
    if outputfile is not None:
        # Write plot output file. Ensure that output directory exists:
        # influenced by http://stackoverflow.com/a/12517490
        if not os.path.exists(os.path.dirname(outputfile)):
            try:
                os.makedirs(os.path.dirname(outputfile))
            except OSError as exc:  # guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        plt.savefig(outputfile)
    else:
        plt.show()
