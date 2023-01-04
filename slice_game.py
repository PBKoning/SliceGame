# -------
# IMPORTS
# -------

import pygame
from constants import *                 # The constants contain the game settings
from trail import Trail                 # The trail is shown when touching the screen
from game_logic import GameLogic
from menu import Menu                   

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

        # Hide mouse if set
        if HIDE_MOUSE:
            pygame.mouse.set_visible(False)

        # Setup clock for fixed fps
        self.fps_clock = pygame.time.Clock()

        # ---------
        # VARIABLES
        # ---------

        # Init objects for trail and menu
        self.trail = Trail(canvas=self.screen, 
                           color_scheme=TRAIL_COLOR_SCHEME, 
                           width=TRAIL_CIRCLE_WIDTH, 
                           max_length=MAX_LEN_TRAIL)

        self.game_logic = GameLogic(canvas=self.screen)

        self.game_menu = Menu(canvas=self.screen, max_len_trail=MAX_LEN_TRAIL)

        # Init the gamestate
        self.game_state = "menu" # Possible gamestates: menu; running; game-over; adjust-screen-orientation

    def draw_screen(self):
        # Background
        self.screen.fill(BG_COLOR) 

        # Trail
        self.trail.draw()

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