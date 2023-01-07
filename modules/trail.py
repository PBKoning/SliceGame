import pygame

class Trail:

    def __init__(self, canvas, color_scheme, width=10, max_length=50, scale_factor=1):
        
        # init variables
        self.canvas = canvas
        self.color_scheme = color_scheme
        self.width = int(width * scale_factor)
        self.max_length = max_length
        
        self.trail = []
        self.old_pos = None

    def update(self):

        # Get mouse info
        self.mouse_click = pygame.mouse.get_pressed()
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        # Create and handle trail
        if self.mouse_click[0]: 
            # Mouse is pressed

            if not self.old_pos:
                # There is no old position
                self.old_pos = pygame.mouse.get_pos() # Store current position as old position
                self.trail.append(self.old_pos)       # Add this position to trail
                
            else:
                # Get new position of mouse
                self.new_pos = pygame.mouse.get_pos()
                
                # Calculate distance between old and new position
                distance =  ((self.old_pos[0] - self.new_pos[0])**2 + (self.old_pos[1] - self.new_pos[1])**2)**0.5
                
                # add extra position(s) in the trail if distance > circle width
                if distance > self.width:  
                    extra_positions = int(distance/self.width)  # Calculate the number of extra circles to add
                    factor_part = 1/(extra_positions+1)  # Calculate the factor part: for 1 extra circle it's 0.5;
                                                        # for 2 extra circles it's 0.333; for 3 extra circles is 0.25; etc.
                                                        # This is used to calculate the x and y of the extra circle
                    # Add the extra positions 
                    for i in range(extra_positions):
                        factor = (i+1)*factor_part  # Calculate the factor to add pixels to the old x and y position
                        extra_x = self.old_pos[0] + (self.new_pos[0]-self.old_pos[0])*factor # Calculate the x position                                                                           
                        extra_y = self.old_pos[1] + (self.new_pos[1]-self.old_pos[1])*factor # Calculate the y position
                        self.trail.append((int(extra_x), int(extra_y))) # Append the position to the trail                

                self.trail.append(self.new_pos) # Append the new position to the trail
                self.old_pos = self.new_pos     # Set the old position to the current position

            # Shorten trail if it's too long
            while len(self.trail) > self.max_length:
                    del self.trail[0]
        else:
            # No mouse press
            self.old_pos = None         # Delete the old position
            for i in range(4):     # Shorten the trail         
                if len(self.trail) > 0:
                    del self.trail[0]

    def get_len(self):
        return len(self.trail)

    def draw(self):
        
        # Draw circles, where first in trail is the smallest and the last the biggest
        for i in range(len(self.trail)):
            diameter = i/self.max_length*self.width # Calculate diameter according to place in trail
            pygame.draw.circle(self.canvas, self.color_scheme[0], self.trail[i], diameter*2)   # Outer circle
            pygame.draw.circle(self.canvas, self.color_scheme[1], self.trail[i], diameter*1.5) # Middle circle
            pygame.draw.circle(self.canvas, self.color_scheme[2], self.trail[i], diameter)     # Inner circle