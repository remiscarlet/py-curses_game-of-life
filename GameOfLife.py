#!/usr/bin/env python3
import time
import random
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
    """
    Will generate an empty board of size BOARD_SIDE_LENGTH all initialized to False

    Returns:
    A 2d list
    """
    board = []
    for i in range(BOARD_SIDE_LENGTH):
        row = [False] * BOARD_SIDE_LENGTH
        board.append(row)

    return board


def logBoard(board):
    for row in board:
        row_str = map(lambda cell_state: "O" if cell_state else ".", row)

        logger.info("".join(row_str))


def getNextGeneration(board):
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
                and new_x > -1
                and new_y < BOARD_SIDE_LENGTH
                and new_y > -1
                and board[y + dy][x + dx]
            ):
                alive_neighbors += 1

    return alive_neighbors


def drawBoard(stdscr, board):
    global CURR_GENERATION
    for y in range(BOARD_SIDE_LENGTH):
        for x in range(BOARD_SIDE_LENGTH):
            symbol = " "
            if board[y][x]:
                symbol = "O"
            stdscr.addch(x, y, symbol)

    stdscr.addstr(BOARD_SIDE_LENGTH, 0, f"Generation #{CURR_GENERATION}")

    stdscr.refresh()


def getRandomCellState():
    return random.randint(0, 1)


def initializeBoard(board):
    for y in range(BOARD_SIDE_LENGTH):
        for x in range(BOARD_SIDE_LENGTH):
            board[y][x] = getRandomCellState()

    return board


BOARD_SIDE_LENGTH = None
GENERATION_DELAY_TIME = 0.1
MAX_GENERATIONS = 1000
CURR_GENERATION = 1


def main(stdscr):
    """
    TODOs:
    - Add some borders/text to UI
    - Refactor/code quality considerations
    """
    global CURR_GENERATION, MAX_GENERATIONS
    global BOARD_SIDE_LENGTH
    curses.curs_set(False)
    stdscr.clear()
    stdscr.refresh()

    BOARD_SIDE_LENGTH = (
        min(stdscr.getmaxyx()) - 1
    )  # Very bottom row will be used for generation count text

    board = generateEmptyBoard()
    board = initializeBoard(board)
    logBoard(board)
    drawBoard(stdscr, board)

    while CURR_GENERATION < MAX_GENERATIONS:
        board = getNextGeneration(board)
        drawBoard(stdscr, board)
        CURR_GENERATION += 1

        time.sleep(GENERATION_DELAY_TIME)


curses.wrapper(main)
