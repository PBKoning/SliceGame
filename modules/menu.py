import pygame
from modules.utilities import *

# Constants
HIGHSCORE_OFFSET = 100
SPACE_AFTER_HIGHSCORE = 25

class Menu:

    def __init__(self, canvas, max_len_trail, width, height, scale_factor, number_images, image_number_width):

        self.canvas = canvas
        self.max_len_trail = max_len_trail
        self.scale_factor = scale_factor
        self.number_images = number_images
        self.image_number_width = image_number_width
        self.image_offset = int(HIGHSCORE_OFFSET * self.scale_factor)
        self.space_after_highscore = int(SPACE_AFTER_HIGHSCORE * self.scale_factor)
        print(self.space_after_highscore)

        # Load and scale  highscore image
        self.img_highscore = pygame.image.load(r'./images/highscore.png').convert_alpha()
        self.img_highscore = scale_image_by_factor(self.img_highscore, scale_factor)      

        # Load and scale start button image
        self.start_button = pygame.image.load(r'./images/start.png').convert_alpha()
        self.start_button = scale_image_by_factor(self.start_button, scale_factor) 
        
        # Init coördinates of the image so it is centered        
        self.start_button_x = (width/2) - (self.start_button.get_width()/2)
        self.start_button_y = (height/2) - (self.start_button.get_height()/2)
        
        # Init variable of start button rectangle
        self.start_button_rect = pygame.Rect(0,0,0,0)
        

    def draw(self, high_score):

        # Highscore
        self.canvas.blit(self.img_highscore, (self.image_offset, self.image_offset))
                
        tmp = str(high_score)
        for count, i in enumerate(tmp):
            int_i = int(i)
            self.canvas.blit(self.number_images[int_i], (self.image_offset + (self.image_number_width * count) + self.img_highscore.get_width() +  self.space_after_highscore, self.image_offset))

        # Draw menu an store the returned rectangle. This is needed to see if mousse is pressed on image
        self.start_button_rect = self.canvas.blit(self.start_button, (self.start_button_x, self.start_button_y))

    def touched(self, trail_length):

        self.trail_length = trail_length

        # Get mouse info
        self.mouse_click = pygame.mouse.get_pressed()
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        # Return if mouse is pressed on menu image and if trail has certain length so it needs to be sliced
        if self.mouse_click[0] and self.trail_length > self.max_len_trail/2: 
            # Mouse is pressed
            return self.start_button_rect.collidepoint(self.mouse_x, self.mouse_y)