# SliceGame
SliceGame is game based on Fruit Ninja, build with Python and PyGame
It can be played with a touchscreen, but also using a mouse. To play it on an Android device you can use PyDroid

**Note** 
This game isn´t very optimized and PyGame is not the worlds fastest game engine, so I suggest playing it fullscreen on slower devices.  
I experienced less stuttering playing it fullscreen. 

# Changelog
30-12-2022 (1): First version with a simple startscreen and a trail when you swipe the screen

30-12-2022 (2): Changed the startbutton

31-12-2022: Added first testversion of a moving target

01-01-2023 (1): Moving target can be touched and gets chopped

01-01-2023 (2): Corrected the rectangle area for slice target

02-01-2023: Target is now a png-image

03-01-2023: Target chopped parts corrected for going from right to left. Images load with convert_alpha(). Trail is also visible when menu is shown. Menu button needs to be sliced.

04-01-2023 (1): Added HIDE_MOUSE to constants.py

04-01-2023 (2): The main program is converted to a class. Added the GameLogic class that handles the targets, score, mistakes, etc. For now it throws 3 targets and repeats this whan these have completed their flight.

04-01-2023 (3): Fixed an error in deleting targets from the list

05-01-2023 (1): Added scaling for different screen sizes and a warning screen if screen is in portrait mode

05-01-2023 (2): Added scoring to game logic (scores are only printed to console for now)

05-01-2023 (3): Increased FPS from 60 to 144 to make movements more smooth. Also added the option to show FPS.

05-01-2023 (4): Decreased FPS to 60 again as it was slowing down the game on slower devices.

06-01-2023: Added scaling of font of FPS on screen. Trail is now always on foreground.

07-01-2023 (1): Moved all modules except 'slice_game.py' to a dedicated modules folder.

07-01-2023 (2): Improved game logic: added bombs that end the game if chopped and game ends after to much mistakes

07-01-2023 (3): Number of missed targets is shown on screen

08-01-2023 (1): Score is shown on screen

08-01-2023 (2): Added a dedicated bomb image and changed a target image into a fruit image

08-01-2023 (3): Added a game-over screen

09-01-2023: Added a lemon, fixed an error in deleting targets: bomb was not on the temp list, causing it to dissapear all of a sudden sometimes.