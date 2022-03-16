import pyautogui as auto
import pygame
import pygame_widgets as pw
from pygame_widgets.slider import Slider
import random
import numpy
from collections import namedtuple
import sys

DISPLAY_WIDTH = 700
DISPLAY_HEIGHT = 600


class game:

    def __init__(self):
        self.width = DISPLAY_WIDTH
        self.height = DISPLAY_HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snek Game")
        pygame.init()

    def draw(self, color=(0, 0, 0)):
        self.window.fill(color)


class Block:

    def __init__(self, t, l, w, h):
        bound = namedtuple('Bound', ['left', 'top', 'width', 'height'])
        self.bound = bound(l, t, w, h)
        self.color = (random.randint(0, 255),
                      random.randint(0, 255),
                      random.randint(0, 255))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bound)

    def updateColor(self, row, col, size, screenshot):
        red = numpy.mean(screenshot[row * size:row * size + size, col * size:col * size + size, 0])
        green = numpy.mean(screenshot[row * size:row * size + size, col * size:col * size + size, 1])
        blue = numpy.mean(screenshot[row * size:row * size + size, col * size:col * size + size, 2])
        if numpy.isnan(red) == False and numpy.isnan(green) == False and numpy.isnan(blue) == False:
            self.color = (int(red), int(green), int(blue))


class Grid:

    def __init__(self):
        self.pixels = []
        self.imageWidth = 800
        self.imageHeight = 500
        self.imageTop = 300
        self.imageLeft = 600
        self.screenshot = None

    def update(self, sizePercentage):
        top = DISPLAY_HEIGHT * .1
        left = DISPLAY_WIDTH * .1
        width = DISPLAY_WIDTH * .7
        height = DISPLAY_HEIGHT * .7

        self.screenshot = auto.screenshot("test.png",
                                     region=[self.imageLeft, self.imageTop, self.imageWidth, self.imageHeight])
        self.screenshot = numpy.array(self.screenshot)

        pixelSize = int(sizePercentage * self.imageWidth)
        imageHeight = int(self.imageHeight / pixelSize)
        imageWidth = int(self.imageWidth / pixelSize)

        displayWidth = int(sizePercentage * width)
        displayHeight = int(sizePercentage * height)

        self.pixels = [
            [Block(j * (displayHeight + 2) + top, i * (displayWidth + 2) + left, displayWidth, displayHeight) for i in
             range(imageWidth)]
            for j in range(imageHeight)]
        for row in range(len(self.pixels)):
            for col in range(len(self.pixels[row])):
                self.pixels[row][col].updateColor(row, col, pixelSize, self.screenshot)

    def draw(self):
        for row in range(len(self.pixels)):
            for col in range(len(self.pixels[row])):
                self.pixels[row][col].draw(main.window)

    def isFishing(self):
        avgBlue = numpy.mean(self.screenshot[:,:,2])
        return avgBlue > 50

    def fishAngry(self):
        redEnough = self.screenshot[(self.screenshot[:,:,0] >= 90) & (self.screenshot[:,:,0] < 150)]
        filtered = redEnough[ (redEnough[:,2] < 40) & (redEnough[:,1] < 40)]

        return len(filtered) != 0


main = game()
grid = Grid()

slider = Slider(main.window, int(DISPLAY_WIDTH * .05),
                int(DISPLAY_HEIGHT * .01),
                int(DISPLAY_WIDTH * .30),
                int(DISPLAY_HEIGHT * .025),
                initial=20,
                min=5,
                max=100,
                step=5,
                handleColour=(250, 50, 50))

# colorChange(blocks)
gameState = "SCANNING"
try:
    with open("data.txt") as fin:
        data = fin.readline().split(',')
        grid.imageTop = int(data[0])
        grid.imageLeft = int(data[1])
        grid.imageWidth = int(data[2])
        grid.imageHeight = int(data[3])
except:
    print("No Data")


while True:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            with open("data.txt",'w') as fout:
                fout.write("{},{},{},{}".format(
                    grid.imageTop,
                grid.imageLeft,
                grid.imageWidth,
                grid.imageHeight
                ))

            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            gameState = "CALLIBRATE"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            auto.mouseInfo()

        if gameState == "CALLIBRATE" and event.type == pygame.MOUSEBUTTONDOWN:
            gameState = "CALLIBRATE2"
            grid.imageTop = auto.position()[1]
            grid.imageLeft = auto.position()[0]
            startClick = (pygame.mouse.get_pos()[1], pygame.mouse.get_pos()[0])

        if gameState == "CALLIBRATE2" and event.type == pygame.MOUSEBUTTONUP:
            gameState = "SCANNING"

            grid.imageHeight = auto.position()[1] - grid.imageTop
            grid.imageWidth = auto.position()[0] - grid.imageLeft

    main.draw()

    # if sliderValue != slider.getValue():

    if gameState == "SCANNING":
        grid.update(slider.getValue() / (DISPLAY_WIDTH / 2))
        grid.draw()
    elif gameState == "CALLIBRATE":
        main.draw((255, 0, 0))
    elif gameState == "CALLIBRATE2":
        main.draw((255, 255, 0))
        pygame.draw.rect(main.window, (255, 0, 0), (grid.imageLeft,
                                                    grid.imageTop,
                                                    pygame.mouse.get_pos()[0] - grid.imageLeft,
                                                    pygame.mouse.get_pos()[1] - grid.imageTop))
    if grid.isFishing():
        if grid.fishAngry() == True:
            main.draw((255, 0, 0))
            auto.mouseUp(button='right')
        else:
            main.draw((0, 255, 250))
            auto.mouseDown(button='right')




    pw.update(events)
    pygame.display.update()
