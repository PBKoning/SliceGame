# -------
# IMPORTS
# -------

import pygame
from constants import *                 # The constants contain the game settings
from trail import Trail                 # The trail is shown when touching the screen
from game_logic import GameLogic
from menu import Menu      
from rotate_screen import RotateScreen             

class SliceGame:

    def __init__(self):
        
        # -----------
        # INIT PYGAME
        # -----------
        
        pygame.init()

        # Setup screen 
        if FULLSCREEN:
            # Fullscreen
            screen_info = pygame.display.Info()
            self.screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
        else:
            # Windowed game 
            self.screen = pygame.display.set_mode(WINDOW_SIZE)

        # Store width and heigth of Pygame screen. This may be different then expected when using PyDroid on an Android phone
        self.screen_width, self.screen_height = self.screen.get_size()
        if self.screen_height > self.screen_width:  # Swap if in portrait mode. This may occur when using PyDroid.
            self.screen_width, self.screen_height = self.screen_height, self.screen_width

        # Calculate the scale factor according to the window size 
        scale_factor_width = self.screen_width / DEFAULT_WINDOW_SIZE[0]
        scale_factor_height = self.screen_height / DEFAULT_WINDOW_SIZE[1]        
        if scale_factor_width < scale_factor_height:
            self.scale_factor = scale_factor_width
        else: 
            self.scale_factor = scale_factor_height
        

        # Hide mouse if set
        if HIDE_MOUSE:
            pygame.mouse.set_visible(False)

        # Setup clock for fixed fps
        self.fps_clock = pygame.time.Clock()

        # ---------
        # VARIABLES
        # ---------

        # Init objects
        self.trail = Trail(canvas=self.screen, 
                           color_scheme=TRAIL_COLOR_SCHEME, 
                           width=TRAIL_CIRCLE_WIDTH, 
                           max_length=MAX_LEN_TRAIL,
                           scale_factor=self.scale_factor)

        self.game_logic = GameLogic(canvas=self.screen,
                                     scale_factor=self.scale_factor)

        self.game_menu = Menu(canvas=self.screen, 
                              max_len_trail=MAX_LEN_TRAIL,
                              width=self.screen_width,
                              height=self.screen_height,
                              scale_factor=self.scale_factor
                              )

        self.rotate_screen = RotateScreen(canvas=self.screen,                               
                                          width=self.screen_width,
                                          height=self.screen_height,
                                          scale_factor=self.scale_factor)

        # Init the gamestate
        self.game_state = self.old_game_state = "menu" # Possible gamestates: menu; running; game-over; portrait-mode

    def draw_screen(self):
        # Background
        self.screen.fill(BG_COLOR) 

        # Trail
        self.trail.draw()

        # If in portrait mode show image to rotate screen
        if self.game_state == "portrait-mode":
            self.rotate_screen.draw()

        # All that belongs to the running game (targets, score, missed targets, ...)    
        if self.game_state == "running":
            self.game_logic.draw()

        if self.game_state == "menu":
            self.game_menu.draw() 

        pygame.display.flip()           # Show new screen

    def run(self):
        
        running = True
        while running:

            # Handle events
            for event in pygame.event.get():
                # Quit by pressing the X button of the window
                if event.type == pygame.QUIT:
                    running = False

            # Check if window is in portrait mode        
            if self.game_state == "portrait-mode":
                # If in portrait mode, check if not in portrait mode anymore                
                w, h = self.screen.get_size()
                if w > h:
                    self.game_state = self.old_game_state # Restore the old game state if not portrait mode anymore
            else:    
                w, h = self.screen.get_size()
                if h > w:
                    self.old_game_state = self.game_state # Store the old game state
                    self.game_state = "portrait-mode"

            # Update trail
            self.trail.update()

            # Update game logic when game is running (targets, score, mistakes, ...)
            if self.game_state == "running":
                self.game_logic.update()                    

            # Handle menu when it is shown
            if self.game_state == "menu":
                if self.game_menu.touched(self.trail.get_len()):
                    self.game_state = "running"
            
            self.draw_screen()
            self.fps_clock.tick(GAME_FPS)   # Limit framerate to 60 FPS

if __name__ == "__main__":
    game = SliceGame()
    game.run()