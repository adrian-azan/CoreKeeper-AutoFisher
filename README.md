pip installs needed:

pip install PyAutoGUI
pip install pygame
pip install numpy
pip install pygame-widgets


Values in data.txt: top,left,width,height

Ok this requires some calibrating so heres what I recommend.

Set your game to windowed mode - Borderless full screen
The program needs to know the x,y coordinates of the fishing gauge. The data.txt file included works well on mine (1920x1080) but you may need to calibrate. If you do need to, heres how:

	Method 1:
	While fishing, click on the pygame window and click m. this will bring up another window 
    that gives you mouse info. Take note of the x and y coordinate of the top left and bottom
    right corner of your fishing gauge. Then do some math and enter the values into data.txt
    as described above.

	Method 2:
	Move the pygame window over the fishing guage, cover it up, but in a way where you can still
	have an idea of where it is behind the window.

	with pygame selected, press C and the pygame will turn red. Left-Click where you believe the top-left
	corner of the fishing guage is, then the pygame will turn yellow. Still holding, drag your mouse to
	the bottom-right corner of the hidden gauge. then just let go. Odds are you will have to refine

	Try fishing, the pygame should turn blue when you have a fish on the line. You can view the test.png 		image to see what pygame is currently examining. You can tweak the values in data.txt to get as 		accurately as you can to the.
