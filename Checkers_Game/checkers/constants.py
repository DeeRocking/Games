"""
This module contains all the constants used throughout the game
"""
import pygame

WIDTH, HEIGHT = 720, 720
SIDEBAR_WIDTH = 250
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0,0)
GREY = (128, 128, 128)
DARK_BLUE = (15, 5, 255)
DARK_RED = (250, 5, 5)

CROWN = pygame.transform.scale(
pygame.image.load("assets/crown.png"),
    (44, 25)
)

WINNER_MEDAL = pygame.transform.scale(
pygame.image.load("assets/medal.png"),(300, 300)
)