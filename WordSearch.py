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
import os


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
    dimensions = len(data[line_n].strip('\n'))  # Length of first line
    if dimensions < 1:
        raise DataError("Unexpected file format")
    for line_n, line in enumerate(data):
        if len(line.strip('\n')) != dimensions:
            break
    else:
        raise DataError("Unexpected file format")
    # Here line_n should point to the empty line separating puzzle and words list
    if re.search("[^\s]", data[line_n]):
        raise DataError("Incorrect file format at line {}".format(line_n+1))
    if dimensions != line_n:
        raise DataError("Incorrect dimensions {}x{}. Square expected.".format(dimensions, line_n))
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


def match_2d(puzzle, row, col, word):
    """
    Match word in current position in 4 directions
    :param puzzle:
    :param row:
    :param col:
    :param word:
    :return: Tuple x, y end coordinates or None
    """

    # Directions - left, down, right, up
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    word = bytearray(word)

    # Check starting point first
    if puzzle[row][col] != word[0]:
        return None

    # Dimensions
    dim = len(puzzle)

    # Search in multiple directions
    for x, y in dirs:
        ri = row
        ci = col
        for ch in word[1:]:
            ri += x
            ci += y
            if ri < 0 or ri == dim or ci < 0 or ci == dim:
                break
            if ch != puzzle[ri][ci]:
                break
        else:
            return ri, ci
    return None


def search_word(puzzle, word):
    dim = len(puzzle)
    for row in range(0, dim):
        for col in range(0, dim):
            coord = match_2d(puzzle, row, col, word)
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
    # Sort words by length to prevent words crossings
    # not needed if crossings are allowed
    for word in sorted(words, key=len, reverse=True):
        coord = search_word(puzzle, word)
        if coord is not None:
            (col, row), (x, y) = coord
            found[word] = ((col, row), (y, x))

            # Uppercase found word to exclude them from further search
            # Not needed since crossings are allowed
            # for ri in range(row, x+1) if x > row else range(x, row+1):
            #     for ci in range(col, y+1) if y > col else range(y, col+1):
            #         puzzle[ri][ci] = chr(puzzle[ri][ci]).upper()
    return found


def format_results(words, found):
    result = []
    for word in words:
        if word in found:
            (r, c), (x, y) = found[word]
            result.append("{} ({}, {}) ({}, {})".format(word.upper(), r+1, c+1, x+1, y+1))
        else:
            result.append("{} not found".format(word.upper()))
    return result


def main(args, loglevel):
    """
    Main function.
    :param args: List of arguments from argparse
    :param loglevel:
    :return:
    """
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    # Section that loads data
    try:
        # Open .pzl file
        with open(args.puzzle_file, 'r') as f:
            # Read data from pzl file
            data = f.readlines()
        # Parse data
        puzzle, words = read_data_from_list(data)

        found = search_words(puzzle, words)
        result = format_results(words, found)
        out_file_name, _ = os.path.splitext(args.puzzle_file)
        with open(out_file_name + ".out", 'w') as f:
            # Write result in output file
            f.write('\n'.join(result))

        logging.debug(result)

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
