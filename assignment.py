#!/usr/bin/env python2
"""
Solar Analytics code assignment
"""
from __future__ import print_function

__author__ = "Yaroslav Hovorunov"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import logging


class DataError(Exception):
    """Incorrect data exception"""
    pass


def read_data_from_file(pzlfile):
    """
    Reads data from a list or stream.

    :param pzlfile: A file with puzzle
    :return: Tuple (puzzle, words)
    :raises: DataError, ValueError
    """
    puzzle = None
    words = None
    return puzzle, words


def sanitize_data(puzzle, words):
    """
    Sanitizes and formats input data.
    :param puzzle:
    :param words:
    :return: puzzle_dims
    """
    if len(puzzle) < 1:
        raise DataError("Data is looped, expected Tree or Forest")


def print_results(words, found):
    pass

def main(args, loglevel):
    """
    Main function.
    :param args: List of arguments from argparse
    :param loglevel:
    :return:
    """
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    # List of words to find
    words = None

    # List of strings representing puzzle
    puzzle = None

    # List of coordinates tuples of found words
    found = None

    # Section that loads data
    try:
        # Open .pzl file
        with open(args.puzzle_file, 'r') as pzlfile:
            # Read data from pzl file
            puzzle, words = read_data_from_file(pzlfile)

        # Sanitize input data
        dimensions = sanitize_data(puzzle, words)

    except (DataError, ValueError) as err:
        logging.error("Cannot read file {} - {}".format(args.data_file, err))
        exit(1)
    except OSError as err:
        logging.error("Cannot open file {} - {}".format(args.data_file, err.strerror))
        exit(err.errno)
    except Exception:
        logging.exception("Unexpected error")
        exit(1)


# Standard code to parse arguments and call the main() function to begin
# the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Looks up for words in a puzzle file")
    parser.add_argument(
        "puzzle_file",
        help="A text file containing puzzle and hidden words")
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase log verbosity",
        action="store_true")
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
