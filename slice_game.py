import pygame

from modules.game_constants import *            # The constants in this module contain the game settings
from modules.trail import Trail                 # The trail is shown when touching the screen
from modules.game_logic import GameLogic
from modules.menu import Menu      
from modules.game_over import GameOver
from modules.rotate_screen import RotateScreen             

class SliceGame:
    """Class that creates a visual game made with PyGame.

    The goal of the game is to slice al fruit object and avoid the bomb object.
    """


    def __init__(self):
        """Initialize the class"""

        # Init the PyGame module (screen, settings, etc.)
        self.init_pygame()
        
        # Load background image and scale it to window size
        self.img_background = pygame.image.load(r'./images/background.png')
        self.img_background = pygame.transform.scale(self.img_background, (self.screen_width, self.screen_height))

        # Init the objects for the game
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

        # Init the gamestate. The possible gamestates are: menu; running; game-over; portrait-mode
        self.game_state = self.old_game_state = "menu"

    def init_pygame(self):
        """Init the PyGame module and make al settings according to it."""
        
        pygame.init()

        # Setup screen: windowed or fullscreen
        if FULLSCREEN:
            screen_info = pygame.display.Info()
            self.screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(WINDOW_SIZE)

        # Store width and heigth of the screen. 
        # This may be different then expected when using PyDroid on an Android phone
        self.screen_width, self.screen_height = self.screen.get_size()
        if self.screen_height > self.screen_width:  # Swap if in portrait mode. This may occur when using PyDroid.
            self.screen_width, self.screen_height = self.screen_height, self.screen_width

        # Calculate the scale factor according to the default window size 
        scale_factor_width = self.screen_width / DEFAULT_WINDOW_SIZE[0]
        scale_factor_height = self.screen_height / DEFAULT_WINDOW_SIZE[1]        
        if scale_factor_width < scale_factor_height:
            self.scale_factor = scale_factor_width
        else: 
            self.scale_factor = scale_factor_height
        
        # Hide or show the mouse
        if HIDE_MOUSE:
            pygame.mouse.set_visible(False)

        # Setup font used for showing the FPS
        pygame.font.init() 
        self.fnt_arial = pygame.font.SysFont('Arial', int(50 * self.scale_factor))

        # Setup clock for fixed fps
        self.fps_clock = pygame.time.Clock()

    def draw_screen(self):
        """Draws al the elements of the game."""

        # Background
        if SHOW_BACKGROUND_IMAGE:
            self.screen.blit(self.img_background, (0, 0))
        else:
            self.screen.fill(BG_COLOR) 

        # Show FPS in window caption and on screen
        if SHOW_FPS:
            str_fps = "fps: " + str(int(self.fps_clock.get_fps()))
            pygame.display.set_caption(str_fps)
            textsurface = self.fnt_arial.render(str_fps, False, (0, 128, 21))
            self.screen.blit(textsurface,(0,0))

        # If in portrait mode show image to rotate screen
        if self.game_state == "portrait-mode":
            self.rotate_screen.draw()

        if self.game_state == "running":
            self.game_logic.draw()
            self.trail.draw()

        if self.game_state == "menu":
            self.game_menu.draw(self.game_logic.get_highscore()) 
            self.trail.draw()
        
        # If gamestate is game-over, also draw the targets and the trail 
        if self.game_state == "game-over":
            self.game_logic.draw()
            self.trail.draw()           
            self.game_over.draw(self.game_logic.get_new_highscore())
            
        # Show new screen
        pygame.display.flip()           

    def run(self):
        """Main function of the game with a continious loop"""
        
        running = True
        while running:

            # Handle events
            for event in pygame.event.get():               
                if event.type == pygame.QUIT:
                    running = False

            # Handle screen in portrait mode       
            if self.game_state == "portrait-mode":
                # If in portrait mode, check if not in portrait mode anymore                
                w, h = self.screen.get_size()
                if w > h:
                    self.game_state = self.old_game_state # Restore the old game state if not in portrait mode anymore
            else:    
                w, h = self.screen.get_size()
                if h > w:
                    self.old_game_state = self.game_state # Store the old game state
                    self.game_state = "portrait-mode"

            # Always update the trail, except when the game is over
            if not self.game_state == "game-over":
                self.trail.update()

            if self.game_state == "running":
                self.game_logic.update(self.trail.get_len())             
                if self.game_logic.get_game_over() == True:
                    self.game_over.set_wait_ticks(GAME_OVER_WAIT_TICKS) 
                    self.game_state = "game-over"   

            if self.game_state == "menu":
                if self.game_menu.start_game(self.trail.get_len()):
                    self.game_logic.reset()
                    self.game_state = "running"
            
            if self.game_state == "game-over":
                if self.game_over.update() == "Done":
                    self.game_state = "menu"

            self.draw_screen()
            self.fps_clock.tick(GAME_FPS)   # Limit framerate 

if __name__ == "__main__":
    game = SliceGame()
    game.run()