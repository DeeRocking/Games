""" This module contains the class that defines the chess pieces """

import pygame

from .constants import RED, WIDTH, SQUARE_SIZE, GREY, WHITE, CROWN


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.column = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0

        self.calculate_position()

    def calculate_position(self):
        """ This method calculates the position of the piece
        in the chess board system based on their row and column.
        """
        self.x = SQUARE_SIZE * self.column + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        """ This method allows set a piece to be a king """
        self.king = True

    def draw(self, win):
        """ This method draws the piece """

        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, WHITE, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

        if self.king:
            win.blit(CROWN,
                     (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height()//2))


    def move(self, row, col):
        """ This method moves the piece to a target (row, col) position"""
        self.row = row
        self.column = col
        self.calculate_position()

    def __repr__(self):
        return str(self.color)