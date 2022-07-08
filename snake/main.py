import pygame
import os
import sys

from walls import Walls
from snake import Snake
from apple import *
from tkinter import *
from constants import *

# center the window
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Snake')

walls_list = Walls.create_list(Walls(), CELL_SIZE)


def print_text(font, text, color, text_position=None):
    font = pygame.font.SysFont(font[0], font[1])
    text = font.render(text, 1, color)
    if text_position is None:
        text_position = text.get_rect(center_x=W/2, center_y=H/2)
    screen.blit(text, text_position)


def draw_text():
    text = "Apples: {}\n Points: {} \nLives: {}".format(apple.count, hero.points, "-" * hero.lives)
    print_text(SCORE_FONT, text, TURQUOISE, (10, 10))


def write_file():
    try:
        f = open("results.txt", "r")
        
        # how many the same names are already in file with results?
        n = f.read().count(player_name) + 1
        f.close()

    except FileNotFoundError:
        f = open("results.txt", "a")
        f.close()
        n = 0

    f = open("results.txt", "a")
    f.write("{} {} {} \n".format(player_name + str(n), apple.count, hero.points))
    f.close()


def draw_walls():
    for wall in walls_list:
        pygame.draw.rect(screen, pygame.Color("blue"), wall, 0)
       
       
def countdown():
    pass