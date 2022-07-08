import pygame
from constants import *


class Walls(object):

    def create_list(self, size):
        """
        Creates a list of wall Rect objects.
        """

        walls = []
        walls.append(pygame.Rect((x, y), (width, height)))
        walls.append(pygame.Rect((100, 70), (280, size)))
        walls.append(pygame.Rect((100, 200), (280, size)))

        # top wall
        walls.append(pygame.Rect((0,0), (W, size)))

        # right wall
        walls.append(pygame.Rect((W - size, 0), (size, H)))

        # bottom wall
        walls.append(pygame.Rect((0, H - size), (W, size)))

        # left wall
        walls.append(pygame.Rect((0, 0), (size, H)))


        return walls