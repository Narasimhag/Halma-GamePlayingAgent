# Halma-GamePlayingAgent

# Description

In this project, we will play the game of Halma, an adversarial game with some similarities to checkers. The game uses a 16x16 checkered gameboard. Each player starts with 19 game pieces clustered in diagonally opposite corners of the board. To win the game, a player needs to transfer all of their pieces from their starting corner to the opposite corner, into the positions that were initially occupied by the opponent. Note that this original rule of the game is subject to spoiling, as a player may choose to not move some pieces at all, thereby preventing the opponent from occupying those locations. Note that the spoiling player cannot win either (because some pieces remain in their original corner and thus cannot be used to occupy all positions in the opposite corner). Here, to prevent spoiling, the goal of the game is to occupy all of the opponent’s starting positions which the opponent is not still occupying. See http://www.cyningstan.com/post/922/unspoiling-halma for more about this rule modification.

For more details on Halma, click [here](https://en.wikipedia.org/wiki/Halma).

This agent solves the 2 player variant of Halma. A typical setup is as follows:


- Simple wooden pawn-style playing pieces, often called "Halma pawns."
- The board consists of a grid of 16×16 squares.
- Each player's camp consists of a cluster of adjacent squares in one corner of the board.
These camps are delineated on the board.
- For two-player games, each player's camp is a cluster of 19 squares. The camps are in
opposite corners.
- Each player has a set of pieces in a distinct color, of the same number as squares in each
camp.
- The game starts with each player's camp filled by pieces of their own color.

# Usage

The handler.py plays the game between agents created by halma.py. Cool part is your agent can also be in Java and handler takes care. Place both th files in same directory and execute handler.py, like this `python3 handler.py`



