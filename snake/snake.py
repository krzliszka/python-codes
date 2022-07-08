import pygame
from constants import *


class Snake(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))

        # snake has three tiles initially - at the beginning it show up in the middle of the screen vertically
        self.body = [
            
        ]