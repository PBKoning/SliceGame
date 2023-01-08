import pygame, random, os
from modules.slice_target import Slice_Target   
from modules.utilities import *

# ------------------------
# CONSTANTS FOR GAME LOGIC
# ------------------------

WAIT_TICKS = 60  # Number of ticks to wait before new targets are added
MAX_MISSED_TARGETS = 3 # Number of targets to miss for game to end (game also ends for a higher number)
TEST_MODE = True # Test mode to set values for targets flights (x-speed, y-speed, gravity, ...)
OFFSET = 100 # Distance to borders for score and missed targets

class GameLogic:

    def __init__(self, canvas, width, height, scale_factor):
        self.canvas=canvas
        self.width = width
        self.height = height
        self.scale_factor = scale_factor
        self.image_offset = int(OFFSET * self.scale_factor)

        self.load_images() 

        self.reset() # Reset score, number of missed targets and empty the target list
        
    def reset(self):
        self.score = 0
        self.missed_targets = 0
        self.game_over = False

        self.targets = [] # List of active targets

        self.wait_counter = 0 # counter 


    def update(self):

        self.update_targets()

        if self.missed_targets >= MAX_MISSED_TARGETS:
            self.game_over = True
        
        # Add targets if there are no more targets
        if len(self.targets) == 0:
            self.wait_counter += 1
            if self.wait_counter >= WAIT_TICKS:
                self.add_targets()                                              
                self.wait_counter = 0


    def update_targets(self):
        '''
        Update all targets, score and mistakes. Remove targets from list if flight is completed.
        
        '''

        # Get mouse position and state of buttons
        mouse_x, mouse_y  = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        tmp_list = [] # Create a temporary list for deleting targets with a complete flight (status: succes or failed)
        for target in self.targets:
            # Update te target
            target.update(mouse_x, mouse_y, mouse_click[0])

            # Handle bombs
            if target.type == "bomb":       
                # If a bomb is chopped the game is over          
                if target.status == "chopped":
                    self.game_over = True   
                # If flight of the bomb is complete (e.g. status is "failed") then delete this target from the list
                if target.status == "failed":  
                    tmp_list.append("delete") # delete this target from the list 

            # Handle normal targets    
            else:   
                # If chopped add to score and mark target as 'scored'             
                if target.status == "chopped" and target.scored == False:                    
                    self.score += 1
                    target.scored = True                    

                # If flight has ended add mistake if not chopped and delete target from target list   
                if target.status == "succes" or target.status == "failed":
                    if target.status == "failed":                    
                        self.missed_targets += 1                        
                    tmp_list.append("delete") # delete this target from the list
                else: 
                    tmp_list.append("keep")   # keep this target in the list              

        # Delete all targets that have a complete flight
        for count, value in enumerate(tmp_list): # replace target in the target list whith the string value "delete"
            if value == "delete":
                self.targets[count] = "delete"

        while "delete" in self.targets:             # delete all elements in the target list with the value "delete"
            self.targets.remove("delete")

    def load_images(self):
        
        # Load image for bomb
        path_bomb_image = "./images/bomb.png"
        self.bomb_image = pygame.image.load(path_bomb_image).convert_alpha()
        self.bomb_image = scale_image_by_factor(self.bomb_image, self.scale_factor)
        self.bomb_images = (self.bomb_image, None, None) # To add images to target object. Sliced images are never used for a bomb.

        # Load number images for score
        self.number_images = []
        
        for i in range(10):
            path_number_image = f"./images/numbers/{i}.png"  
            img_number = pygame.image.load(path_number_image).convert_alpha()
            img_number = scale_image_by_factor(img_number, self.scale_factor)
            self.number_images.append(img_number)
                
        self.image_number_width = self.number_images[0].get_width()    

        # Load images to show missed targets
        self.missed_targets_images = []
        
        for i in range(4):
            path_missed_target_image = f"./images/missed_targets_{i}.png"  
            img_missed_target = pygame.image.load(path_missed_target_image).convert_alpha()
            img_missed_target = scale_image_by_factor(img_missed_target, self.scale_factor)
            self.missed_targets_images.append(img_missed_target)
                
        self.image_missed_target_width = self.missed_targets_images[0].get_width()

        # Targets
        self.target_images = []
        count = 0
        
        loading = True
        while loading:            
            path_target = f"./images/targets/target_{count}.png"  
            path_target_slice_left = f"./images/targets/target_{count}_slice_left.png"  
            path_target_slice_right = f"./images/targets/target_{count}_slice_right.png"  
            if os.path.exists(path_target):
                img_target = pygame.image.load(path_target).convert_alpha()
                img_target = scale_image_by_factor(img_target, self.scale_factor)
                img_target_slice_left = pygame.image.load(path_target_slice_left).convert_alpha()
                img_target_slice_left = scale_image_by_factor(img_target_slice_left, self.scale_factor)
                img_target_slice_right = pygame.image.load(path_target_slice_right).convert_alpha()
                img_target_slice_right = scale_image_by_factor(img_target_slice_right, self.scale_factor)

                self.target_images.append((img_target, img_target_slice_left, img_target_slice_right))
            else:
                loading = False
            count += 1

    def add_targets(self):       

        if TEST_MODE == True:         
            # Test mode can be used to set values for targets flights (x-speed, y-speed, gravity, ...)
            # The same target(s) will appear every time
            self.targets.append(Slice_Target(canvas=self.canvas, 
                                            x_pos=0 * self.scale_factor,          #random.randint(600, 900), 
                                            x_speed=random.randint(3, 7) * self.scale_factor,        #random.randint(0.5, 3.5), 
                                            y_pos=1300 * self.scale_factor, 
                                            y_speed=-20 * self.scale_factor,        #random.randint(-16,-12), 
                                            gravity=0.15 * self.scale_factor, 
                                            type="normal",
                                            images=self.target_images[1]))   
            self.targets.append(Slice_Target(canvas=self.canvas, 
                                            x_pos=1920 * self.scale_factor,          #random.randint(600, 900), 
                                            x_speed=random.randint(-12, -2) * self.scale_factor,        #random.randint(-4, -2), 
                                            y_pos=1300 * self.scale_factor, 
                                            y_speed=-34 * self.scale_factor,        #random.randint(-16,-12), 
                                            gravity=0.45 * self.scale_factor, 
                                            type="bomb",
                                            images= self.bomb_images ))                                            
            # self.targets.append(Slice_Target(canvas=self.canvas,
            #                                     x_pos=random.randint(100, 200), 
            #                                     x_speed=random.randint(1, 4), 
            #                                     y_pos=1300,
            #                                     y_speed=random.randint(-11, -9), 
            #                                     gravity=0.10, 
            #                                     width=30, 
            #                                     images=target_images))   
            # self.targets.append(Slice_Target(canvas=self.canvas,
            #                                     x_pos=random.randint(400, 500), 
            #                                     x_speed=random.randint(-2, 2), 
            #                                     y_pos=1300,
            #                                     y_speed=random.randint(-11, -9), 
            #                                     gravity=0.10, 
            #                                     width=30, 
            #                                     images=target_images))              
            

    def draw(self):
        
        # Missed targets    
        self.canvas.blit(self.missed_targets_images[self.missed_targets], (self.width - self.image_missed_target_width- self.image_offset, self.image_offset))         

        # Score        
        tmp = str(self.score)
        for count, i in enumerate(tmp):
            int_i = int(i)
            self.canvas.blit(self.number_images[int_i], (self.image_offset + (self.image_number_width * count), self.image_offset)) # (

        # Targets
        for target in self.targets:
            target.draw()     
        