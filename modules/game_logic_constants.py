# ------------------------
# CONSTANTS FOR GAME LOGIC
# ------------------------

WAIT_TICKS = 60  # Number of ticks to wait before new targets are added
SHOW_NEW_HIGHSCORE_TICKS = 60
MAX_MISSED_TARGETS = 3 # Number of targets to miss for game to end (game also ends for a higher number)
TEST_MODE = False # Test mode to set values for targets flights (x-speed, y-speed, gravity, ...)
OFFSET = 100 # Distance to borders for score and missed targets
MAX_TARGET_DELAY = 60 # Maximum number of ticks to wait before target starts

TARGET_START_SETTINGS = [

    # Fastest targets

     {"x_pos":0,
     "x_speed_min":1,
     "x_speed_max":15,
     "y_pos":1300,
     "y_speed":-47, 
     "gravity":0.80},

     {"x_pos":480,
     "x_speed_min":1,
     "x_speed_max":12,
     "y_pos":1300,
     "y_speed":-47, 
     "gravity":0.80},

     {"x_pos":960,
     "x_speed_min":1,
     "x_speed_max":8,
     "y_pos":1300,
     "y_speed":-47, 
     "gravity":0.80},

     {"x_pos":960,
     "x_speed_min":-9,
     "x_speed_max":-1,
     "y_pos":1300,
     "y_speed":-47, 
     "gravity":0.80},

     {"x_pos":1440,
     "x_speed_min":-12,
     "x_speed_max":-1,
     "y_pos":1300,
     "y_speed":-47, 
     "gravity":0.80},

     {"x_pos":1850,
     "x_speed_min":-16,
     "x_speed_max":-3,
     "y_pos":1300,
     "y_speed":-47, 
     "gravity":0.80},


    # Faster targets

    {"x_pos":0,
     "x_speed_min":1,
     "x_speed_max":14,
     "y_pos":1300,
     "y_speed":-40, 
     "gravity":0.60},

    {"x_pos":480,
     "x_speed_min":1,
     "x_speed_max":10,
     "y_pos":1300,
     "y_speed":-40, 
     "gravity":0.60},

    {"x_pos":960,
     "x_speed_min":1,
     "x_speed_max":7,
     "y_pos":1300,
     "y_speed":-40, 
     "gravity":0.60},

    {"x_pos":960,
     "x_speed_min":-8,
     "x_speed_max":-1,
     "y_pos":1300,
     "y_speed":-40, 
     "gravity":0.60},

     {"x_pos":1440,
     "x_speed_min":-11,
     "x_speed_max":-1,
     "y_pos":1300,
     "y_speed":-40, 
     "gravity":0.60},

     {"x_pos":1850,
     "x_speed_min":-14,
     "x_speed_max":-3,
     "y_pos":1300,
     "y_speed":-40, 
     "gravity":0.60},



    # Normal speed targets

    {"x_pos":0,
     "x_speed_min":1,
     "x_speed_max":12,
     "y_pos":1300,
     "y_speed":-34, 
     "gravity":0.45},
     
     {"x_pos":480,
     "x_speed_min":1,
     "x_speed_max":9,
     "y_pos":1300,
     "y_speed":-34, 
     "gravity":0.45},

     {"x_pos":960,
     "x_speed_min":1,
     "x_speed_max":6,
     "y_pos":1300,
     "y_speed":-34, 
     "gravity":0.45},

     {"x_pos":960,
     "x_speed_min":-7,
     "x_speed_max":-1,
     "y_pos":1300,
     "y_speed":-34, 
     "gravity":0.45},

     {"x_pos":1440,
     "x_speed_min":-10,
     "x_speed_max":-1,
     "y_pos":1300,
     "y_speed":-34, 
     "gravity":0.45},

     {"x_pos":1850,
     "x_speed_min":-13,
     "x_speed_max":-3,
     "y_pos":1300,
     "y_speed":-34, 
     "gravity":0.45},

    # Slowest targets

    #  {"x_pos":0,
    #  "x_speed_min":1,
    #  "x_speed_max":7,
    #  "y_pos":1300,
    #  "y_speed":-20, 
    #  "gravity":0.15},

    #  {"x_pos":480,
    #  "x_speed_min":1,
    #  "x_speed_max":5,
    #  "y_pos":1300,
    #  "y_speed":-20, 
    #  "gravity":0.15},

    #  {"x_pos":960,
    #  "x_speed_min":1,
    #  "x_speed_max":3,
    #  "y_pos":1300,
    #  "y_speed":-20, 
    #  "gravity":0.15},

    #  {"x_pos":960,
    #  "x_speed_min":-4,
    #  "x_speed_max":-1,
    #  "y_pos":1300,
    #  "y_speed":-20, 
    #  "gravity":0.15},

    #  {"x_pos":1440,
    #  "x_speed_min":-6,
    #  "x_speed_max":-1,
    #  "y_pos":1300,
    #  "y_speed":-20, 
    #  "gravity":0.15},

    #  {"x_pos":1800,
    #  "x_speed_min":-7,
    #  "x_speed_max":-1,
    #  "y_pos":1300,
    #  "y_speed":-20, 
    #  "gravity":0.15},

]
