# Algorithm to solve the towers of hanoi in a minimum amount of moves
# Adam Snoyman, adamsnoyman@gmail.com, September 2021

import pygame
import asyncio

FPS = 60
SLEEP = 300

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
        rings.append(Ring(n, i, 0, n - i))
    return rings

def drawWindow(window, rings, n):
    drawBackground(window)
    for i in range(n):
        rings[i].draw(window, min(15, 175 // n), min(25, 499 // n))
    pygame.display.flip()
    pygame.event.pump()

async def moveStack(window, rings, size, n, start, empty, end):
    await asyncio.sleep((SLEEP // n) / 1000) 

    # If the stack of rings is empty, return
    if size == 0:
        return

    # Move the stack (except the bottom ring) to the empty peg
    await moveStack(window, rings, size - 1, n, start, end, empty)

    await asyncio.sleep((SLEEP // n) / 1000)  

    # Move the next ring to the goal
    rings[size - 1].peg = end

    tally = 0
    for i in range(n):
        if rings[i].peg == end:
            tally += 1
    rings[size - 1].height = tally

    drawWindow(window, rings, n)

    await asyncio.sleep((SLEEP // n) / 1000)

    # Move the stack to the goal
    await moveStack(window, rings, size - 1, n, empty, start, end)

async def main():

    clock = pygame.time.Clock()
    pygame.init()  

    n = 4
    window = pygame.display.set_mode((1400, 700))
    # Get number of rings
    font = pygame.font.Font(None, 32)
    text = 'Enter number of rings: '
    input = '' 
    run = True
    while run:
        window.fill(GREY)
        for event in pygame.event.get():
            clock.tick(FPS)
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input.strip().isnumeric():
                        n = int(input.strip())
                        run = False
                    else:
                        text = "Enter a whole number of rings: "
                elif event.key == pygame.K_BACKSPACE:
                    input = input[:-1]
                else:
                    input += event.unicode
        
        txt_surface = font.render(text + input, True, BLACK)
        window.blit(txt_surface, (300, 100))
        pygame.display.flip()
        await asyncio.sleep(0)

    rings = makeRings(n)
    drawWindow(window, rings, n)

    await moveStack(window, rings, n, n, 0, 1, 2)

    run = True
    while run:
        for event in pygame.event.get():
            clock.tick(FPS)
            if event.type == pygame.QUIT:
                run = False
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())