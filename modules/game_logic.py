import pygame, random, os
from modules.slice_target import Slice_Target   
from modules.utilities import *
from modules.game_logic_constants import *  


class GameLogic:

    def __init__(self, canvas, max_len_trail, width, height, scale_factor):
        self.canvas=canvas
        self.max_len_trail = max_len_trail
        self.width = width
        self.height = height
        self.scale_factor = scale_factor
        self.image_offset = int(OFFSET * self.scale_factor)

        self.load_images() 

        # Load sounds
        self.chop_sound = pygame.mixer.Sound("./sounds/slice.wav")             
        self.explosion_sound = pygame.mixer.Sound("./sounds/explosion.wav")
        self.missed_sound = pygame.mixer.Sound("./sounds/missed.wav")
        self.game_over_sound = pygame.mixer.Sound("./sounds/game-over.wav")

        self.reset() # Reset score, number of missed targets and empty the target list
        
    def reset(self):
        self.score = 0
        self.missed_targets = 0
        self.game_over = False

        self.targets = [] # List of active targets

        self.wait_counter = 0 # counter 


    def update(self, trail_length):

        self.trail_length_factor = trail_length / self.max_len_trail # Needed to see if a target is touched and not sliced
        
        self.update_targets()

        if self.missed_targets >= MAX_MISSED_TARGETS:
            self.game_over = True
            pygame.mixer.Sound.play(self.game_over_sound) 
        
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
            target.update(mouse_x, mouse_y, mouse_click[0], self.trail_length_factor)

            # Handle bombs
            if target.type == "bomb":       
                # If a bomb is chopped the game is over          
                if target.status == "flying":
                    tmp_list.append("keep")   # keep this target in the list  
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
                        if self.missed_targets < MAX_MISSED_TARGETS:   # Play missed target sound, but not the last time,...
                            pygame.mixer.Sound.play(self.missed_sound) # ...the last time the game-over sound is played                    
                    tmp_list.append("delete") # delete this target from the list
                else: 
                    tmp_list.append("keep")   # keep this target in the list as it is still flying (chopped or not)            

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
        self.bomb_images = (self.bomb_image, self.bomb_image, self.bomb_image) # To add images to target object. Sliced images are never used for a bomb.

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
                                            x_pos=1850 * self.scale_factor,     
                                            x_speed=-3 * self.scale_factor,     
                                            y_pos=1300 * self.scale_factor, 
                                            y_speed=-47 * self.scale_factor,    
                                            gravity=0.80 * self.scale_factor, 
                                            type="bomb",
                                            images=self.bomb_images,
                                            sound=self.explosion_sound,
                                            delay=random.randint(0, MAX_TARGET_DELAY)))               
            
        if TEST_MODE != True:

            number_of_targets = random.randint(1, 2)
            max_bombs = 1

            if self.score > 2:
                number_of_targets = random.randint(2, 3)
                max_bombs = 1

            if self.score > 10:
                number_of_targets = random.randint(2, 4)
                max_bombs = 1    

            if self.score > 20:
                number_of_targets = random.randint(2, 5)
                max_bombs = 2

            if self.score > 30:
                number_of_targets = random.randint(3, 6)
                max_bombs = 2  

            if self.score > 30:
                number_of_targets = random.randint(4, 7)
                max_bombs = 2       
                        
            number_of_bombs = 0 # Count number of bombs that are added to not exceed max number
            for i in range(number_of_targets):
                c = random.randint(0, len(TARGET_START_SETTINGS)-1) # random choice of the target start settings for flight
            
                if random.randint(0, 1) == 1 and number_of_bombs < max_bombs :
                    number_of_bombs += 1
                    # add bomb
                    self.targets.append(Slice_Target(canvas=self.canvas, 
                                                    x_pos=TARGET_START_SETTINGS[c]["x_pos"] * self.scale_factor,                                             
                                                    x_speed= random.randint(TARGET_START_SETTINGS[c]["x_speed_min"],TARGET_START_SETTINGS[c]["x_speed_max"]) * self.scale_factor+random.choice((-1,1)),     
                                                    y_pos=TARGET_START_SETTINGS[c]["y_pos"] * self.scale_factor, 
                                                    y_speed=TARGET_START_SETTINGS[c]["y_speed"] * self.scale_factor,    
                                                    gravity=TARGET_START_SETTINGS[c]["gravity"] * self.scale_factor, 
                                                    type="bomb",
                                                    images=self.bomb_images,
                                                    sound=self.explosion_sound,
                                                    delay=random.randint(0, MAX_TARGET_DELAY)))     
                else:   
                    # add fruit
                    self.targets.insert(0, Slice_Target(canvas=self.canvas, 
                                                    x_pos=TARGET_START_SETTINGS[c]["x_pos"] * self.scale_factor,                                             
                                                    x_speed= random.randint(TARGET_START_SETTINGS[c]["x_speed_min"],TARGET_START_SETTINGS[c]["x_speed_max"]) * self.scale_factor,     
                                                    y_pos=TARGET_START_SETTINGS[c]["y_pos"] * self.scale_factor, 
                                                    y_speed=TARGET_START_SETTINGS[c]["y_speed"] * self.scale_factor,    
                                                    gravity=TARGET_START_SETTINGS[c]["gravity"] * self.scale_factor, 
                                                    type="normal",
                                                    images=self.target_images[random.randint(0, len(self.target_images)-1)],
                                                    sound=self.chop_sound,
                                                    delay=random.randint(0, MAX_TARGET_DELAY)))     


    def draw(self):
        
        # Missed targets  ;
        if self.missed_targets > 3 :
            self.missed_targets = 3  # If > 3 the right image can not be shown
        self.canvas.blit(self.missed_targets_images[self.missed_targets], (self.width - self.image_missed_target_width- self.image_offset, self.image_offset))         

        # Score        
        tmp = str(self.score)
        for count, i in enumerate(tmp):
            int_i = int(i)
            self.canvas.blit(self.number_images[int_i], (self.image_offset + (self.image_number_width * count), self.image_offset)) #             

        # Targets        
        for target in self.targets:
            target.draw()     
            
        