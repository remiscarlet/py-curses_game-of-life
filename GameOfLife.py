#!/usr/bin/env python3

import curses
from curses import wrapper


import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")

file_handler = logging.FileHandler("GameOfLife.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def generateEmptyBoard():
    board = []
    for i in range(BOARD_SIDE_LENGTH):
        row = [False] * BOARD_SIDE_LENGTH
        board.append(row)

    return board


def printBoard(board):
    print("=" * BOARD_SIDE_LENGTH)
    for row in board:
        # We'll want to figure out a "prettier" way to print
        """
        def translateCellStateToString(cell_state):
          if cell_state:
            return "O"
          else:
            return " "
        """

        row_str = map(lambda cell_state: "O" if cell_state else ".", row)

        print("".join(row_str))
    print("=" * BOARD_SIDE_LENGTH)


def progressGeneration(board):
    next_board = generateEmptyBoard()

    for x in range(BOARD_SIDE_LENGTH):
        for y in range(BOARD_SIDE_LENGTH):
            next_board[y][x] = getCellState(board, x, y)

    return next_board


def getCellState(board, x, y):
    """
    Return boolean (T/F) of whether given cell is alive or dead based on our four rules

    1. If a given cell has exactly 3 neighbors, considered alive (whether originally dead or alive)
    2. If a given cell has >3 neighbors, overpop -> dead
    3. If a given cell has 2 neighbors and alive, stays alive
    4. If a given cell has <2 neighbors and is alive, dies

    if cell dead:
      if neighbors are 3:
        cell becomes alive
      else:
        still dead :(

    if cell alive:
      if neighbors<2:
        cell dies
      if neighbors are 2 or 3:
        still alive
      if neighbors>3
        cell dies


    """

    curr_cell = board[y][x]
    neighbor_count = checkNeighbors(board, x, y)

    if curr_cell:
        if neighbor_count < 2:
            return False
        elif neighbor_count in (2, 3):
            return True
        elif neighbor_count > 3:
            return False
    else:
        if neighbor_count == 3:
            return True
        else:
            return False


def checkNeighbors(board, x, y):
    alive_neighbors = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue

            new_x, new_y = x + dx, y + dy
            if (
                new_x < BOARD_SIDE_LENGTH
                and new_y < BOARD_SIDE_LENGTH
                and board[y + dy][x + dx]
            ):
                # TODO: Does wrapping the board affect the gamerules?
                alive_neighbors += 1

    return alive_neighbors


def drawBoard(stdscr, board):
    """
    stdscr.addch(3, 0, "H")
    stdscr.addch(3, 1, "i")
    stdscr.addch(3, 2, "!")

    [.       v- (x:1,y:0)
      [" ", "O", " "],
      ["O", "O", "O"],
      [" ", " ", " "],
    ]

    board[0][1]
    x0, y1
    y1, x0

    """
    for y in range(BOARD_SIDE_LENGTH):
        for x in range(BOARD_SIDE_LENGTH):
            symbol = " "
            if board[y][x]:
                symbol = "O"
            stdscr.addch(x, y, symbol)
    stdscr.refresh()


def initializeBoard(board):
    """
    TODO: Randomize intiial board
    """
    board[3][4] = True
    board[2][3] = True
    board[0][3] = True
    board[0][2] = True
    board[0][4] = True

    return board


BOARD_SIDE_LENGTH = 10

GENERATIONS = 2


def main():
    global GENERATIONS
    stdscr = curses.initscr()
    stdscr.clear()
    stdscr.refresh()

    board = generateEmptyBoard()
    board = initializeBoard(board)
    drawBoard(stdscr, board)

    while GENERATIONS > 0:
        board = progressGeneration(board)
        drawBoard(stdscr, board)
        GENERATIONS -= 1


main()