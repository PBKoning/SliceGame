# -------
# IMPORTS
# -------

import pygame
from constants import * # All constants
from trail import Trail # The trail class
from menu import Menu   # The menu class

# -----------
# INIT PYGAME
# -----------

pygame.init()

# Setup screen
if FULLSCREEN:
    # Fullscreen
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
else:
    # Window
    screen = pygame.display.set_mode(WINDOW_SIZE)

# Hide mouse
pygame.mouse.set_visible(False)

# Setup clock for constant fps
fps_clock = pygame.time.Clock()

# ---------
# VARIABLES
# ---------

# Init objects for trail and menu
trail = Trail(canvas=screen, color_scheme=(DARK_BLUE, BLUE, LIGHT_BLUE), width=TRAIL_CIRCLE_WIDTH, max_length=MAX_LEN_TRAIL)
game_menu = Menu(canvas=screen)

game_state = "menu" # Possible gamestates: menu; running

# --------
# MAINLOOP
# --------

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        # Quit by pressing the X button of the window
        if event.type == pygame.QUIT:
            running = False
    
    if game_state == "running":
        # Handle mouse for trail
        trail.handle_mouse()

    if game_state == "menu":
        if game_menu.touched():
            game_state = "running"
    
    # -----------
    # Draw screen
    # -----------

    # Background
    screen.fill(BG_COLOR) 

    if game_state == "running":
        # Trail    
        trail.draw()

    if game_state == "menu":
        game_menu.draw() 

    pygame.display.flip() # Show new screen
    fps_clock.tick(60)        # Limit framerate to 60 FPS