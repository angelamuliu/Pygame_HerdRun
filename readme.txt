

###############################


HERD RUN - GAME
amliu (D) 15112
images, sound, code created by Angela Liu
Music > Bits of Happiness: Andersson187 @ Newgrounds (licensed under CC)


###############################



>>> INSTALLATION & RUNNING

1) Download ZIP file
2) Extract ZIP file into location of your choice
3) File will run correctly IF files are of this order:
	> herdGame.py, object_creator.py, Util.py, images folder, and sound folder in same local folder

>>> INSTALLING PYGAME
Herd Run uses pygame 1.9.2pre.win-amd64-py27.exe, AKA pygame 1.9.2, pre-release for 64 bit windows.
If you use a 32 bit PC, please try to download this version first. If it does not work, try downloading pygame 1.9.1.win32-py2.7.msi instead: http://www.pygame.org/download.shtml

4) Install 64-bit version of pygame: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame
5) Follow the instructions provided in the pygame installation package. More help can be found here:
http://www.pygame.org/install.html

6) Run herdGame.py by clicking on it once you are ready to play

Notes: You must have python 2.7.2 and pygame 1.9.2 installed to run the game. Game is not guaranteed to run on newer or older versions of python. Game is not guaranteed to run on newer or older versions of pygame, in addition, you should try to download the correct pygame for optimal performance. Game is not guaranteed to run perfectly on a MAC. Game is not guaranteed to run perfectly on a 32 bit computer.

If crashing persists, please check out the troubleshooting section found at the bottom of the readme file.



###############################



>>>INTRO

Herd Run is a fun action game with strategic elements mixed in! The goal is to reach the next point goal in order to move on to the next level. Points are earned by dropping cows into a pen area. You can see how many points you have in the top left corner, as well as your point goal. 

However, watch the time...The game is over when the time runs out!

The timer is always ticking down. But in addition to that, a crafty monster is out to eat your cows! Whenever it eats a cow, you lose a significant chunk of time. And when you collide with the monster, it's so unpleasant you lose time for that as well! Part of your focus will go to picking and dropping off cows into the pen for points. But the rest goes to PREVENTING the monster from eating your cows...and your precious time!

Luckily, you're a hardy herder and you've got some tricks up your sleave. Your fire wall trap slows the monster in a goopy lava mess. You can also send zap rays at the monster to stun it. And you've also got some tasty hamburgers that will distract the monster from targeting animals (oh dear, where did those hamburgers come from though).

Between levels, you can pause and take a breather. In addition, you can UPGRADE one of your statistics to make it better! How will you play the game? What stats will you upgrade?

Lets see how high you can score! Save ALL the animals!



###############################



>>> CONTROLS

* Use arrow keys to move the herder
* Bump into cows to pick them off
* If holding cow, bump into pen zone to drop off for points

A -> drop animal
S -> fire wall (slows monster to 1/3 of normal speed)
D -> zap attack (if hits, freezes monster for set amount of time)
F -> food decoy (monster stops chasing animals and heads over to decoy)
SPACE -> use powerup

~ If holding cow, you cannot use attacks. You CAN use powerups, however.
~ Attacks require staimina, displayed on left. You cannot attack if you do not have enough staimina.



###############################



>>> TROUBLESHOOTING


* My game is crashing!
	1) Make sure you have followed installation instructions as closely as possible. Files MUST be in relative positions for the game to load images, sound, and functions.
	2) Try downloading a different version of pygame.
	3) Check that images folder has all images. Missing images will cause the game to not load. If you are missing one of the images, please redownload to reattain the missing image. Or contact me for the mising image.
	4) Check that the sound folder has all images. Missing sound files will cause the game to not load.
	5) If none of these solve your problem, please send me the error output and I will look into it. The game should otherwise run.


* My game is lagging...
	Try turning off other programs running in the background. In addition, if using a laptop/macbook, try plugging in your computer. The game should be running at 60 FPS. Signs of lag may also be in part due to high running speed of the herder or monster at later levels.


* The cows are stuck
	Please send me the error output and I will look into it. Please note that the cows, when running from the monster, may panic and bounce off once another.


* The monster is stuck between targeting two or more cows and is spazzing out?
	The monster targets the closest cow. When two cows are the same distance, this may happen. I am still working out the kinks. To fix, please use your food move. Or you can take advantage of this and cheat...but you wouldn't, right?


* I can't use attacks / get past upgrading??
	Check if your caps lock is on. IF it is on, please turn it off.

contact me: amliu@andrew.cmu.edu



###############################


