import pygame
from modules.utilities import *

class GameOver:

    def __init__(self, canvas, width, height, scale_factor):

        self.canvas = canvas        
        self.scale_factor = scale_factor
        self.wait_ticks = 0

        # Load and scale image
        self.game_over_image = pygame.image.load(r'./images/game-over.png').convert_alpha()
        self.game_over_image = scale_image_by_factor(self.game_over_image, scale_factor)       
        
        # Init coördinates of the image so it is centered        
        self.game_over_image_x = (width/2) - (self.game_over_image.get_width()/2)
        self.game_over_image_y = (height/2) - (self.game_over_image.get_height()/2)
    
    def set_wait_ticks(self, wait_ticks):
        self.wait_ticks = wait_ticks

    def update(self):
        self.wait_ticks -= 1
        if self.wait_ticks <= 0:
            return "Done"
        else:
            return "Waiting"    

    def draw(self):
        # Draw menu an store the returned rectangle. This is needed to see if mousse is pressed on image
        self.canvas.blit(self.game_over_image, (self.game_over_image_x, self.game_over_image_y))
