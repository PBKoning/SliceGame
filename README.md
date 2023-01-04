# SliceGame
A touchscreen game based on Fruit Ninja - build with Python and PyGame

30-12-2022 (1): First version with a simple startscreen and a trail when you swipe the screen

30-12-2022 (2): Changed the startbutton

31-12-2022: Added first testversion of a moving target

01-01-2023 (1): Moving target can be touched and gets chopped

01-01-2023 (2): Corrected the rectangle area for slice target

02-01-2023: Target is now a png-image

03-01-2023: Target chopped parts corrected for going from right to left. Images load with convert_alpha(). Trail is also visible when menu is shown. Menu button needs to be sliced.

04-01-2023 (1): Added HIDE_MOUSE to constants.py

04-01-2023 (2): The main program is converted to a class. Added the GameLogic class that handles the targets, score, mistakes, etc. For now it throws 3 targets and repeats this whan these have completed their flight.
