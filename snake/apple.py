import pygame

from constants import *
from random import randrange


class Apple:

    count = 0

    def __init__(self, size):
        self.x = randrange(1, COL_COUNT - 1) # random horizontal position
        self.y = randrange(1, ROW_COUNT - 1) # random vertical position
        self.size = size
        self.rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, self.size, self.size)


    def draw(self, screen):
        # draw red square apple
        pygame.draw.rect(screen, RED, self.rect)


    def set_random_xy(self):
        """
        Function to changing position of apple.
        """
        
        self.x = randrange(1, COL_COUNT-1)
        self.y = randrange(1, ROW_COUNT-1)

        self.rect.x = self.x * CELL_SIZE
        self.rect.y = self.y * CELL_SIZE

        # each 3rd apple is going to be bigger
        if Apple.count%3 == 0:
            self.size = CELL_SIZE + 6
            self.rect.x -= 3
            self.rect.y -= 3
        else:
            self.size = CELL_SIZE 
        self.rect.width = self.size
        self.rect.height = self.size

