# -------
# IMPORTS
# -------

import pygame
from modules.game_constants import *            # The constants contain the game settings
from modules.trail import Trail                 # The trail is shown when touching the screen
from modules.game_logic import GameLogic
from modules.menu import Menu      
from modules.game_over import GameOver
from modules.rotate_screen import RotateScreen             

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
        

        # Load background
        self.img_background = pygame.image.load(r'./images/background.png')
        self.img_background = pygame.transform.scale(self.img_background, (self.screen_width, self.screen_height))

        # Hide mouse if set
        if HIDE_MOUSE:
            pygame.mouse.set_visible(False)

        # setup font
        pygame.font.init() # you have to call this at the start, 
                        # if you want to use this module.
        self.font_arial = pygame.font.SysFont('Arial', int(50*self.scale_factor))

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
                                    max_len_trail=MAX_LEN_TRAIL,
                                    width=self.screen_width,
                                    height=self.screen_height,
                                    scale_factor=self.scale_factor)

        self.game_menu = Menu(canvas=self.screen, 
                              max_len_trail=MAX_LEN_TRAIL,
                              width=self.screen_width,
                              height=self.screen_height,
                              scale_factor=self.scale_factor,
                              number_images = self.game_logic.number_images,            # Use number images from game logic also to project highscore
                              image_number_width = self.game_logic.image_number_width)

        self.game_over = GameOver(canvas=self.screen,
                                  width=self.screen_width,
                                  height=self.screen_height,
                                  scale_factor=self.scale_factor)

        self.rotate_screen = RotateScreen(canvas=self.screen,                               
                                          width=self.screen_width,
                                          height=self.screen_height,
                                          scale_factor=self.scale_factor)

        # Init the gamestate
        self.game_state = self.old_game_state = "menu" # Possible gamestates: menu; running; game-over; portrait-mode

    def draw_screen(self):

        # Background
        if SHOW_BACKGROUND_IMAGE:
            self.screen.blit(self.img_background, (0, 0))
        else:
            self.screen.fill(BG_COLOR) 

        # Show FPS in caption and on screen
        if SHOW_FPS:
            str_fps = "fps: "+str(int(self.fps_clock.get_fps()) )
            pygame.display.set_caption(str_fps)
            textsurface = self.font_arial.render(str_fps, False, (0, 128, 21))
            self.screen.blit(textsurface,(0,0))

        # If in portrait mode show image to rotate screen
        if self.game_state == "portrait-mode":
            self.rotate_screen.draw()

        # All that belongs to the running game (targets, score, missed targets, ...)    
        if self.game_state == "running":
            self.game_logic.draw()
            self.trail.draw()

        if self.game_state == "menu":
            self.game_menu.draw(self.game_logic.get_highscore()) 
            self.trail.draw()
        
        if self.game_state == "game-over":
            self.game_logic.draw()
            self.trail.draw()
            self.game_over.draw(self.game_logic.get_new_highscore())
            

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

            # Update trail always except when game is over
            if not self.game_state == "game-over":
                self.trail.update()

            # Update game logic when game is running (targets, score, mistakes, ...)
            if self.game_state == "running":
                self.game_logic.update(self.trail.get_len())             
                if self.game_logic.game_over == True:
                    self.game_over.set_wait_ticks(180)
                    self.game_state = "game-over"   # >>> TODO: game state "game-over" has to be implemented TODO <<<

            # Handle menu when it is shown
            if self.game_state == "menu":
                if self.game_menu.touched(self.trail.get_len()):
                    self.game_logic.reset()
                    self.game_state = "running"

            # Handle game-over when it is shown
            if self.game_state == "game-over":
                if self.game_over.update() == "Done":
                    self.game_state = "menu"

            self.draw_screen()
            self.fps_clock.tick(GAME_FPS)   # Limit framerate to 60 FPS

if __name__ == "__main__":
    game = SliceGame()
    game.run()