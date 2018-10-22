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
import re


class DataError(Exception):
    """Incorrect data exception"""
    pass


def read_data_from_list(data):
    """
    Reads data from a list or stream.

    :param data: A list with puzzle
    :return: Tuple (puzzle, words)
    :raises: DataError, ValueError
    """
    line_n = 0
    dimensions = len(data[line_n])  # Length of first line
    if dimensions < 2:  # 1 is '\n'
        raise DataError("Unexpected file format")
    for line_n, line in enumerate(data):
        if len(line) != dimensions:
            break
    else:
        raise DataError("Unexpected file format")
    # Here line_n should point to the empty line separating puzzle and words list
    if data[line_n] != "\n":
        raise DataError("Incorrect file format at line {}".format(line_n+1))
    if dimensions - 1 != line_n:  # dimensions include trailing '\n'
        raise DataError("Incorrect dimensions {}x{}. Square expected.".format(dimensions-1, line_n))
    puzzle = [bytearray(ln.lower().strip('\n')) for ln in data[:line_n]]
    words = [ln.lower().strip('\n') for ln in data[line_n+1:] if ln != "\n"]

    # make sure data contains letters only
    nonletters = re.compile("[^\w\s]")
    for i, s in enumerate(puzzle):
        if nonletters.search(s):
            raise DataError("Incorrect file format at line {}".format(i+1))
    for i, s in enumerate(words):
        if nonletters.search(s):
            raise DataError("Incorrect file format at line {}".format(i+line_n+3))

    return puzzle, words


def sanitize_data(puzzle, words):
    """
    Sanitizes and formats input data.
    :param puzzle:
    :param words:
    :return: puzzle_dims
    """
    pass

def search2D(puzzle, row, col, word):

    # Directions - left, down, right, up
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    word = bytearray(word)

    # Check starting point first
    if puzzle[row][col] != word[0]:
        return None

    dim = len(puzzle)

    # Search in multiple directions
    for x, y in dirs:
        for i, ch in enumerate(word[1:], 1):
            ri = row + i * x
            ci = col + i * y
            if ri < 0 or ri == dim or ci < 0 or ci == dim:
                break
            if ch != puzzle[ri][ci]:
                break
        else:
            return ri, ci
    return None


def search_word(puzzle, word):
    dim = len(puzzle)
    for row in xrange(0, dim):
        for col in xrange(0, dim):
            coord = search2D(puzzle, row, col, word)
            if coord is not None:
                return (col, row), coord
    return None


def search_words(puzzle, words):
    """
    Searches for words in puzzle
    :param puzzle:
    :param words:
    :return:
    """

    found = {}
    # Sort words by length
    for word in sorted(words, key=len, reverse=True):
        coord = search_word(puzzle, word)
        if coord is not None:
            (col, row), (x, y) = coord
            found[word] = ((col, row), (y, x))

            # Uppercase found word to exclude them from further search
            # for ri in range(row, x+1) if x > row else range(x, row+1):
            #     for ci in range(col, y+1) if y > col else range(y, col+1):
            #         puzzle[ri][ci] = chr(puzzle[ri][ci]).upper()
    return found


def print_results(words, found):
    for word in words:
        if word in found:
            (r, c), (x, y) = found[word]
            print("{} ({}, {}) ({}, {})".format(word.upper(), r+1, c+1, x+1, y+1))
        else:
            print("{} not found".format(word.upper()))


def main(args, loglevel):
    """
    Main function.
    :param args: List of arguments from argparse
    :param loglevel:
    :return:
    """
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    # List of words to find
    words = []

    # List of strings representing puzzle
    puzzle = []

    # List of coordinates tuples of found words
    found = {}

    # Section that loads data
    try:
        # Open .pzl file
        with open(args.puzzle_file, 'r') as pzlfile:
            # Read data from pzl file
            data = pzlfile.readlines()
        # Parse data
        puzzle, words = read_data_from_list(data)

        # Sanitize input data
        #dimensions = sanitize_data(puzzle, words)

        found = search_words(puzzle, words)
        print_results(words, found)
        print("")
        for i, line in enumerate(puzzle):
            print("{:2}{}".format(i,line))

    except DataError as err:
        logging.error("Cannot read file {} - {}".format(args.puzzle_file, err))
        exit(1)
    except OSError as err:
        logging.error("Cannot open file {} - {}".format(args.puzzle_file, err.strerror))
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
