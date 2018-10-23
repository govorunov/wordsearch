#!/usr/bin/env python3
"""
Unit tests for WordSearch
"""

__author__ = "Yaroslav Hovorunov"
__version__ = "0.1.0"
__license__ = "MIT"

import unittest
from WordSearch import *


class TestReadDataFunctions(unittest.TestCase):
    """ Testing weight_calculator.read_funds_data """

    def test_ok_data1(self):
        """ Testing original assignment data """
        data = """CIRN
            ADOG
            TCIS
            KCOW
            
            CAT
            DOG
            COW"""
        data = [s.strip() for s in data.splitlines()]
        puzzle, words = read_data_from_list(data)
        self.assertListEqual(words, ["cat", "dog", "cow"])
        self.assertListEqual(puzzle, [bytearray("cirn"), bytearray("adog"),
                                      bytearray("tcis"), bytearray("kcow")])

    def test_nonsquare(self):
        """ Testing data is not square """
        data = """CIRN
            ADOG
            TCIS
            
            CAT
            DOG
            COW"""
        data = [s.strip() for s in data.splitlines()]
        self.assertRaises(DataError, read_data_from_list, data)

    def test_spaces(self):
        """ Testing spaces in data """
        data = """C RN
            A OG
            TC S
            KCOW
            
            CAT
            DOG
            COW"""
        data = [s.strip() for s in data.splitlines()]
        puzzle, words = read_data_from_list(data)
        self.assertListEqual(words, ["cat", "dog", "cow"])
        self.assertListEqual(puzzle, [bytearray("c rn"), bytearray("a og"),
                                      bytearray("tc s"), bytearray("kcow")])

    def test_no_words(self):
        """ Testing malformed """
        data = """CIRN
            ADOG
            TCIS
            KCOW"""
        data = [s.strip() for s in data.splitlines()]
        self.assertRaises(DataError, read_data_from_list, data)

    def test_nonsquare2(self):
        """ Testing data is not square """
        data = """CIRN
            ADOG
            TCIS
            COW
            
            CAT
            DOG
            COW"""
        data = [s.strip() for s in data.splitlines()]
        self.assertRaises(DataError, read_data_from_list, data)


class TestSearchAndFormat(unittest.TestCase):
    """ Testing search and format """

    def test_ok_data1(self):
        """ Testing original assignment data """
        data = """CIRN
            ADOG
            TCIS
            KCOW
            
            CAT
            DOG
            COW"""
        data = [s.strip() for s in data.splitlines()]
        puzzle, words = read_data_from_list(data)
        found = search_words(puzzle, words)
        result = format_results(words, found)
        self.assertListEqual(result, ["CAT (1, 1) (1, 3)",
                                      "DOG (2, 2) (4, 2)",
                                      "COW (2, 4) (4, 4)"])

    def test_ok_data2(self):
        """ Testing original assignment data """
        data = """DNOMAID
                PQINEEG
                XXWQTDK
                CDKBRAF
                UWERAFX
                TDAFESJ
                AKJSHHE
                
                DIAMOND
                HEART"""
        data = [s.strip() for s in data.splitlines()]
        puzzle, words = read_data_from_list(data)
        found = search_words(puzzle, words)
        result = format_results(words, found)
        self.assertListEqual(result, ["DIAMOND (7, 1) (1, 1)",
                                      "HEART (5, 7) (5, 3)"])

    def test_ok_data3(self):
        """ Testing original assignment data """
        data = """CIRN
                ADOG
                TCIS
                KDIE
                
                CAT
                DOG
                DUCK"""
        data = [s.strip() for s in data.splitlines()]
        puzzle, words = read_data_from_list(data)
        found = search_words(puzzle, words)
        result = format_results(words, found)
        self.assertListEqual(result, ["CAT (1, 1) (1, 3)",
                                      "DOG (2, 2) (4, 2)",
                                      "DUCK not found"])


class TestEndToEnd(unittest.TestCase):
    """ Testing with files """

    def test_end_to_end1(self):
        """ Testing end to end """
        with open('puzzle1.pzl', 'r') as f:
            # Read data from pzl file
            data = f.readlines()
        puzzle, words = read_data_from_list(data)
        found = search_words(puzzle, words)
        result = format_results(words, found)
        self.assertListEqual(result, ["THE (38, 12) (38, 10)",
                                      "INTERNAL (27, 15) (27, 8)",
                                      "REPRESENTATION (33, 25) (33, 38)",
                                      "OF (17, 6) (17, 5)",
                                      "DATATYPE (14, 31) (7, 31)",
                                      "IS (8, 15) (7, 15)",
                                      "CRITICALLY (34, 8) (25, 8)",
                                      "IMPORTANT (20, 19) (12, 19)",
                                      "WHEN (35, 8) (35, 11)",
                                      "INTERFACING (30, 22) (30, 32)",
                                      "WITH (9, 18) (9, 15)",
                                      "CODE (19, 10) (16, 10)",
                                      "AND (28, 2) (30, 2)",
                                      "SEVERAL (6, 23) (6, 17)",
                                      "FUNCTIONS (11, 20) (11, 12)",
                                      "ARE (36, 10) (38, 10)",
                                      "AVAILABLE (18, 30) (26, 30)",
                                      "TO (35, 2) (35, 3)",
                                      "INSPECT (23, 20) (17, 20)",
                                      "THESE (7, 35) (7, 31)",
                                      "DETAILS (31, 20) (25, 20)"])


if __name__ == '__main__':
    unittest.main()
