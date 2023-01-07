import pygame, random
from modules.slice_target import Slice_Target   
from modules.utilities import *

class GameLogic:

    def __init__(self, canvas, scale_factor):
        self.canvas=canvas
        self.scale_factor = scale_factor

        self.load_images() 

        self.reset() # Reset score, number of missed targets and empty the target list
        
    def reset(self):
        self.score = 0
        self.missed_targets = 0

        self.targets = []

        # >>> TEST
        self.TEST_add_random_targets()
        #     TEST <<<

    def update(self):

        # --------------
        # UPDATE TARGETS
        # --------------

        mouse_x, mouse_y  = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        tmp_list = [] # temporary list for deleting targets with a complete flight (succes or failed)
        for target in self.targets:
            # If chopped add to score and mark target as 'scored'
            target.update(mouse_x, mouse_y, mouse_click[0])
            if target.status == "chopped" and target.scored == False:
                self.score += 1
                target.scored = True
                print(f"Score: {self.score} | Missed targets: {self.missed_targets}") 

            # If flight has ended add mistake if not chopped and delete target from target list   
            if target.status == "succes" or target.status == "failed":
                if target.status == "failed":                    
                    self.missed_targets += 1
                    print(f"Score: {self.score} | Missed targets: {self.missed_targets}")                    
                tmp_list.append("delete") # delete this target from the list
            else: 
                tmp_list.append("keep")   # keep this target in the list  
            

        for count, value in enumerate(tmp_list): # replace target in the target list whith the string value "delete"
            if value == "delete":
                self.targets[count] = "delete"

        while "delete" in self.targets:             # delete all elements in the target list with the value "delete"
            self.targets.remove("delete")


        # >>> TEST
        if len(self.targets) == 0:
            self.TEST_add_random_targets()                                              
        #     TEST <<<

    def load_images(self):
        pass
        
    # >>> TEST    
    def TEST_add_random_targets(self):
        img_target = pygame.image.load(r'./images/target_01.png').convert_alpha()
        img_target = scale_image_by_factor(img_target, self.scale_factor)
        img_target_slice_left = pygame.image.load(r'./images/target_01_slice_left.png').convert_alpha()
        img_target_slice_left = scale_image_by_factor(img_target_slice_left, self.scale_factor)
        img_target_slice_right = pygame.image.load(r'./images/target_01_slice_right.png').convert_alpha()
        img_target_slice_right = scale_image_by_factor(img_target_slice_right, self.scale_factor)

        target_images = (img_target, img_target_slice_left, img_target_slice_right)
        self.targets.append(Slice_Target(canvas=self.canvas, 
                                         x_pos=0 * self.scale_factor,          #random.randint(600, 900), 
                                         x_speed=random.randint(3, 7) * self.scale_factor,        #random.randint(0.5, 3.5), 
                                         y_pos=1300 * self.scale_factor, 
                                         y_speed=-20 * self.scale_factor,        #random.randint(-16,-12), 
                                         gravity=0.15 * self.scale_factor, 
                                         images=target_images))   
        self.targets.append(Slice_Target(canvas=self.canvas, 
                                         x_pos=1920 * self.scale_factor,          #random.randint(600, 900), 
                                         x_speed=random.randint(-12, -2) * self.scale_factor,        #random.randint(-4, -2), 
                                         y_pos=1300 * self.scale_factor, 
                                         y_speed=-34 * self.scale_factor,        #random.randint(-16,-12), 
                                         gravity=0.45 * self.scale_factor, 
                                         images=target_images))                                            
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
    #     TEST <<<

    def draw(self):
        for target in self.targets:
            target.draw()     