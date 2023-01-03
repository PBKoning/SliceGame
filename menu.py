import pygame

class Menu:

    def __init__(self, canvas, max_len_trail):

        self.canvas = canvas
        self.max_len_trail = max_len_trail

        self.start_button = pygame.image.load(r'./images/menu.png').convert_alpha()
        
        # Init coördinates of the image so it is centered
        w, h = canvas.get_size() # get width and height of canvas
        self.start_button_x = (w/2) - (self.start_button.get_width()/2)
        self.start_button_y = (h/2) - (self.start_button.get_height()/2)
        
        # Init variable of start button rectangle
        self.start_button_rect = pygame. Rect(0,0,0,0)
        

    def draw(self):
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