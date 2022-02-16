# Algorithm to play the towers of hanoi in a minimum amount of moves
# Adam Snoyman, adamsnoyman@gmail.com, September 2021

import pygame
import heapq

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
    def __init__(self, i, n, peg):
        self.size = i + 1 # int from 1 - n
        self.colour = COLOURS[i%9] # Picked from COLOURS
        self.peg = peg # int from 0 - 2
        self.height = n - i # int from 1 - n
        self.selected = (0,0) # Relative coordinates from where the mouse clicked
        self.hStep = min(15, 275 // n)
        self.vStep = min(25, 499 // n)

    def draw(self, window):
        pygame.draw.rect(window, self.colour, (300 - self.size * self.hStep + self.peg * 375 + self.selected[1], \
            600 - self.height * self.vStep + self.selected[0], 2 * (self.size * self.hStep) + 25, self.vStep))

    def isOver(self, pos):
        if pos[1] > 600 - self.height * self.vStep and pos[1] < 600 - (self.height - 1) * self.vStep:
            if pos[0] > 300 - self.size * self.hStep + self.peg * 375 and \
                    pos[0] < 325 + self.size * self.hStep + self.peg * 375:
                return True
        return False

def drawBackground():
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
        rings.insert(0, Ring(i, n, 0))
    return rings

def makePegs(rings):
    pegs = []
    pegs.append(Peg(rings, [100, 475, 100, 600]))
    pegs.append(Peg([], [475, 875, 100, 600]))
    pegs.append(Peg([], [875, 1300, 100, 600]))
    return pegs

def selectRing(pos, peg):
    if peg.size > 0 and peg.rings[-1].isOver(pos):
        return True
    return False

def placeRing(pegs, targetPeg, originPeg):
    if targetPeg == originPeg:
        return False
    ring = pegs[originPeg].rings[-1]
    ring.selected = (0,0)
    if pegs[targetPeg].size == 0 or ring.size < pegs[targetPeg].rings[-1].size:
        ring = pegs[originPeg].rings.pop()
        ring.height = pegs[targetPeg].size + 1
        ring.peg = targetPeg
        pegs[targetPeg].rings.append(ring)
        pegs[targetPeg].size += 1
        pegs[originPeg].size -= 1
        return True
    return False

def drawWindow(pegs):
    window = drawBackground()
    for i in range(3):
        for j in range(pegs[i].size):
            pegs[i].rings[j].draw(window)
    pygame.display.update()

def main():

    n = int(input("Enter tower height: "))
    rings = makeRings(n)
    pegs = makePegs(rings)
    drawWindow(pegs)

    clock = pygame.time.Clock()

    coords = None
    origin = None
    drag = False
    tally = 0
    run = True
    while run:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            clock.tick(FPS)
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    rings = makeRings(n)
                    pegs = makePegs(rings)
                    tally = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(3):
                    if selectRing(pos, pegs[i]):
                        origin = i
                        drag = True
                        coords = pos
            elif event.type == pygame.MOUSEMOTION and drag:
                pegs[origin].rings[-1].selected = (pos[1] - coords[1], pos[0] - coords[0])
            elif event.type == pygame.MOUSEBUTTONUP and drag:
                placed = False
                for i in range(3):
                    if pegs[i].isOver(pos):  
                        if placeRing(pegs, i, origin):
                            placed = True
                            tally += 1
                if placed == False:
                    pegs[origin].rings[-1].selected = (0,0)
                drag = False

        if pegs[2].size == n:
            print(f"Congratulations, you finished in {tally} moves!")
            run = False
        drawWindow(pegs)
                

    pygame.quit()

if __name__ == "__main__":
    main()
