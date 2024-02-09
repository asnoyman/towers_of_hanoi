# Algorithm to play the towers of hanoi in a minimum amount of moves
# Adam Snoyman, adamsnoyman@gmail.com, September 2021

import pygame
import sys
import asyncio

from pygame.constants import WINDOWHITTEST

FPS = 60

# Colours used
WHITE = (255, 255, 255)
GREY = (169, 169, 169)
BLACK = (0,0,0)
COLOURS = [(255, 0, 0), (255, 127, 0), (255, 255, 0), \
    (0, 255, 0), (0, 255, 255), (0, 127, 255), \
    (0, 0, 255), (127, 0, 255), (255, 0, 255)]

class Peg:
    def __init__(self, rings, coords):
        self.rings = rings
        self.size = len(rings)
        self.left = coords[0]
        self.right = coords[1]
        self.top = coords[2]
        self.bottom = coords[3]
    
    def isOver(self, pos):
        # pos is the mouse position
        # ie: a tuple of (col,row) coordinates
        if pos[1] > self.top and pos[1] < self.bottom:
            if pos[0] > self.left and pos[0] < self.right:
                return True
        return False

class Ring:
    def __init__(self, i, peg, height, selected):
        self.size = i + 1 # int from 1 - n
        self.colour = COLOURS[i%9] # Picked from COLOURS
        self.peg = peg # int from 0 - 2
        self.height = height # int from 1 - n
        self.selected = selected

    def draw(self, window, hStep, vStep):
        pygame.draw.rect(window, self.colour, (300 - self.size * hStep + self.peg * 375, \
            600 - self.height * vStep, 2 * (self.size * hStep) + 25, vStep))
        if self.selected:
            pygame.draw.rect(window, WHITE, (300 - self.size * hStep + self.peg * 375, \
            600 - self.height * vStep, 2 * (self.size * hStep) + 25, vStep), 3)

def drawBackground(window):
    window.fill(GREY)
    base = pygame.Rect(100, 600, 1200, 25)
    pygame.draw.rect(window, BLACK, base)
    pole1 = pygame.Rect(300, 100, 25, 500)
    pygame.draw.rect(window, BLACK, pole1)
    pole2 = pygame.Rect(675, 100, 25, 500)
    pygame.draw.rect(window, BLACK, pole2)
    pole3 = pygame.Rect(1050, 100, 25, 500)
    pygame.draw.rect(window, BLACK, pole3)

def makeRings(n):
    rings = []
    for i in range(n):
        rings.insert(0, Ring(i, 0, n - i, False))
    return rings

def makePegs(rings):
    pegs = []
    pegs.append(Peg(rings, [100, 475, 100, 600]))
    pegs.append(Peg([], [475, 875, 100, 600]))
    pegs.append(Peg([], [875, 1300, 100, 600]))
    return pegs

def selectRing(peg):
    if peg.size > 0:
        peg.rings[-1].selected = True
        return True
    return False

def placeRing(pegs, targetPeg, originPeg):
    ring = pegs[originPeg].rings[-1]
    if targetPeg == originPeg:
        ring.selected = False
    elif pegs[targetPeg].size == 0 or ring.size < pegs[targetPeg].rings[-1].size:
        ring = pegs[originPeg].rings.pop()
        ring.selected = False
        ring.height = pegs[targetPeg].size + 1
        ring.peg = targetPeg
        pegs[targetPeg].rings.append(ring)
        pegs[targetPeg].size += 1
        pegs[originPeg].size -= 1
        return True
    return False

def drawWindow(window, pegs, n):
    drawBackground(window)
    for i in range(3):
        for j in range(pegs[i].size):
            pegs[i].rings[j].draw(window, min(15, 175 // n), min(25, 499 // n))
    pygame.display.flip()

async def main():

    n = 4

    clock = pygame.time.Clock()
    pygame.init()

    window = pygame.display.set_mode((1400, 700))
    rings = makeRings(n)
    pegs = makePegs(rings)
    drawWindow(window, pegs, n)

    quit = False
    origin = None
    ringSelected = False
    tally = 0
    run = True
    while run:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    rings = makeRings(n)
                    pegs = makePegs(rings)
                    tally = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ringSelected:
                    for i in range(3):
                        if pegs[i].isOver(pos):  
                            if placeRing(pegs, i, origin):
                                ringSelected = False  
                                tally += 1
                            if i == origin:
                                ringSelected = False           
                else:
                    for i in range(3):
                        if pegs[i].isOver(pos):
                            if selectRing(pegs[i]):
                                origin = i
                                ringSelected = True
        if pegs[2].size == n:
            if tally == 2**n - 1:
                print("Congratulations, you finished in the optimal number of moves!!")
            else: 
                print(f"Congratulations, you finished in {tally} moves!")
            run = False
        drawWindow(window, pegs, n)
        clock.tick(FPS)   
        await asyncio.sleep(0)
          

    if quit == True:
        pygame.quit()
        sys.exit()
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

asyncio.run(main())
