"""Post-processing code for hello workd Demo. This code is included with
flowServ for testing purposes only.
"""

from collections import Counter

import argparse
import sys
import time

from flowserv.service.postproc.client import Runs


def main(rundir, k=25, timeout=10, outputfile=None):
    """Create a csv file containing the frequency of the k most frequent
    n-grams in the greeting files of all runs. Counts only those n-grams that
    do not contain a whitespace character.
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
                        if ' ' not in ng:
                            ngrams[ng] += 1
        # Delay execution to allow for testing running post-processing
        # workflows
        time.sleep(timeout)
    # Output csv file with two columns: ngram,count
    with open(outputfile, 'w') as f:
        for ngram, count in ngrams.most_common(k):
            f.write('{},{}\n'.format(ngram, count))


if __name__ == '__main__':
    args = sys.argv[1:]
    # Parse command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--runs", required=True)
    parser.add_argument("-o", "--outputfile", required=True)
    parser.add_argument("-k", "--topk", type=int, required=False, default=25)
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        required=False,
        default=1
    )
    parsed_args = parser.parse_args(args)
    # Run the main routine.
    main(
        rundir=parsed_args.runs,
        k=parsed_args.topk,
        timeout=parsed_args.timeout,
        outputfile=parsed_args.outputfile
    )
