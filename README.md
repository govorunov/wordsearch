# 2D word search

##### Author: Yaroslav Hovorunov
##### License: MIT

A program in Python that locates words in a 2 dimensional grid of letters and outputs the start and end coordinates for each of the words found. The grid has the same number of rows and columns (X*X). Words can appear vertically, horizontally or diagonally, forwards or backwards. If a word is detected twice in the puzzle, only one result is to be reported.

Program can be called with the following command:

    python WordSearch.py puzzle1.pzl

Program takes text file to the input. The input file consists of a grid of letters representing the puzzle, a blank line and a list a words to be searched for, each on a new line. Example of the puzzle1.pzl text file:

    ANTR
    BTOP
    OZXW  
    WLKT  

    BOW
    TOP
    ANT

The program will create puzzle1.out output file, containing list of found words and corresponding coordinates for each word. Each line of the output file is of the following format:

    word (start coord x, start coord y) (end coord x, end coord y)

Example of output file:

    BOW (1, 2) (1, 4)
    TOP (2, 2) (4, 2)
    ANT (1, 1) (3, 1)

If the word is not found in the input puzzle it will be reported in the output file as:

    COW not found
