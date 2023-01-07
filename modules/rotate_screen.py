import pygame
from modules.utilities import *

class RotateScreen:

    def __init__(self, canvas, width, height, scale_factor):
        
        self.canvas = canvas

        # Load and scale image
        self.rotate_screen_image = pygame.image.load(r'./images/rotate_screen.png').convert_alpha()
        self.rotate_screen_image = scale_image_by_factor(self.rotate_screen_image, scale_factor)  

        # Scale image if needed
        # if scale_factor != 1:
        #     old_width, old_height = self.rotate_screen_image.get_size()
        #     print(old_width, old_height)
        #     new_width = int(old_width * scale_factor)
        #     new_height = int(old_height * scale_factor)            
        #     self.rotate_screen_image = pygame.transform.scale(self.rotate_screen_image, (new_width, new_height))

        # Init coördinates of the image so it is centered        
        width, height = height, width # swap these as it is in portrait mode
        self.rotate_screen_image_x = (width/2) - (self.rotate_screen_image.get_width()/2)
        self.rotate_screen_image_y = (height/2) - (self.rotate_screen_image.get_height()/2)

    def draw(self):
        self.canvas.blit(self.rotate_screen_image, (self.rotate_screen_image_x, self.rotate_screen_image_y))
