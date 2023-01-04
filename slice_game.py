# -------
# IMPORTS
# -------

import pygame
from constants import * # All constants
from trail import Trail # The trail class
from slice_target import Slice_Target # The slice target class
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

# Hide mouse if set
if HIDE_MOUSE:
    pygame.mouse.set_visible(False)

# Setup clock for constant fps
fps_clock = pygame.time.Clock()

# ---------
# VARIABLES
# ---------

# Init objects for trail and menu
trail = Trail(canvas=screen, color_scheme=(DARK_BLUE, BLUE, LIGHT_BLUE), width=TRAIL_CIRCLE_WIDTH, max_length=MAX_LEN_TRAIL)

# >>> TEST
img_target = pygame.image.load(r'./images/target_01.png').convert_alpha()
img_target_slice_left = pygame.image.load(r'./images/target_01_slice_left.png').convert_alpha()
img_target_slice_right = pygame.image.load(r'./images/target_01_slice_right.png').convert_alpha()
target_images = (img_target, img_target_slice_left, img_target_slice_right)
test_target = Slice_Target(canvas=screen, x_pos=600, x_speed=-5, y_pos=600, y_speed=-12, gravity=0.15, width=30, images=target_images)
#     TEST <<<

game_menu = Menu(canvas=screen, max_len_trail=MAX_LEN_TRAIL)

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
    
    # Update trail
    trail.update()

    if game_state == "running":
               
        # >>> TEST
        mouse_x, mouse_y  = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        test_target.update(mouse_x, mouse_y, mouse_click[0])
        #     TEST <<<

    if game_state == "menu":
        if game_menu.touched(trail.get_len()):
            game_state = "running"
    
    # -----------
    # Draw screen
    # -----------

    # Background
    screen.fill(BG_COLOR) 

    # Trail    
    trail.draw()

    if game_state == "running":
        # >>> TEST
        test_target.draw()
        #     TEST <<<
        
        

        

    if game_state == "menu":
        game_menu.draw() 

    pygame.display.flip() # Show new screen
    fps_clock.tick(GAME_FPS)        # Limit framerate to 60 FPS