# Algorithm to solve the towers of hanoi in a minimum amount of moves
# Adam Snoyman, adamsnoyman@gmail.com, September 2021

import pygame
import time

FPS = 60

# Colours used
GREY = (169, 169, 169)
BLACK = (0,0,0)
COLOURS = [(255, 0, 0), (255, 127, 0), (255, 255, 0), \
    (0, 255, 0), (0, 255, 255), (0, 127, 255), \
    (0, 0, 255), (127, 0, 255), (255, 0, 255)]

class Ring:
    def __init__(self, n, i, peg, height):
        self.size = i + 1 # int from 1 - n
        self.colour = COLOURS[i%9] # Picked from COLOURS
        # self.colour = (255 - i * 255 // n, 0, i * 255 // n) # for a gradient between red and blue
        self.peg = peg # int from 0 - 2
        self.height = height # int from 1 - n

    def draw(self, window, hStep, vStep):
        pygame.draw.rect(window, self.colour, (300 - self.size * hStep + self.peg * 375, \
            600 - self.height * vStep, 2 * (self.size * hStep) + 25, vStep))

def drawBackground(n):
    window = pygame.display.set_mode((1400, 700))
    window.fill(GREY)
    base = pygame.Rect(100, 600, 1200, 25)
    pygame.draw.rect(window, BLACK, base)
    pole1 = pygame.Rect(300, 100, 25, 500)
    pygame.draw.rect(window, BLACK, pole1)
    pole2 = pygame.Rect(675, 100, 25, 500)
    pygame.draw.rect(window, BLACK, pole2)
    pole3 = pygame.Rect(1050, 100, 25, 500)
    pygame.draw.rect(window, BLACK, pole3)
    return window

def makeRings(n):
    rings = []
    for i in range(n):
        rings.append(Ring(n, i, 0, n - i))
    return rings

def drawWindow(rings, n):
    window = drawBackground(n)
    for i in range(n):
        rings[i].draw(window, min(15, 175 // n), min(25, 499 // n))
    pygame.display.update()

def moveStack(window, rings, size, n, start, empty, end):
    time.sleep(0.1)
    # If the stack of rings is empty, return
    if size == 0:
        return

    # Move the stack one higher to the empty peg
    moveStack(window, rings, size - 1, n, start, end, empty)

    time.sleep(0.1)
    # Move the next bring to the goal
    rings[size - 1].peg = end

    tally = 0
    for i in range(n):
        if rings[i].peg == end:
            tally += 1
    rings[size - 1].height = tally

    drawWindow(rings, n)

    time.sleep(0.1)
    # Move the stack to the goal
    moveStack(window, rings, size - 1, n, empty, start, end)

def main():

    n = int(input("Enter tower height: "))
    window = drawBackground(n)
    rings = makeRings(n)
    drawWindow(rings, n)

    clock = pygame.time.Clock()

    moveStack(window, rings, n, n, 0, 1, 2)

    run = True
    while run:
        for event in pygame.event.get():
            clock.tick(FPS)
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()
