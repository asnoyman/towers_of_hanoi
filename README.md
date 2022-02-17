# Towers of Hanoi
A playble version of the Towers of Hanoi puzzle, in either click and move or drag and drop mode.

There is also a solver if you wish to watch the solution play out for you.

# Preview
![Alt text](ToH_img.png?raw=true "Title")

# Goal
The aim of the Towers of Hanoi is to move the entire stack of discs from the first to last peg. However you can only move one disc at a time (from the top of a stack) and a bigger disc may never be on top of a smaller one.

# Procedures
To play the game, run the code locally of the mode you want to play (click vs drag) and enter a number representing the stack size in the terminal. You will be able to play until the game is complete from here.

To watch a solve, run the solver code and enter a stack size. To edit the speed, change the SLEEP global variable at the top of the file (lower means less sleep, ie: faster). 


# Reason for Project
This was the first time I had used python - before learning it formally in university. I used the experience to learn about classes, general python practise and the pygame module in particular to create a GUI. In particular, I got exposure to utilizing the cursor position and drawing basic figures in code.

I implemented the solver with a recursive algorithm to be as efficient as possible. There is an iterative solution that achieves the same effect however the recursive method is much more intuitive and clean.
