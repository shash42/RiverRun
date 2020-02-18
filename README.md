# RiverRun

This is a 2 player river-themed 3D game (the third dimension is time). Made as an assignment for the Introduction to Software Systems course using Pygame

**Game theme:** <br>
The task of the players is to cross from one side to the other going across multiple "safe" platforms. 
The safe platforms do have some fixed obstacles, namely logs of wood, palm trees and couples cuz this game was developed in Valentine's week (Not being a Bajrang Dal member, you surely don't want to disturb them).
<br>
The river has some moving obstacles: <br>
a) Boat - Slow but big. Right to left.<br>
b) Jet Ski - Fast. Left to Right<br>
c) Crocodile - Medium speed, but only visible when close. Also can eat you if you are on the border of the river-bank. Right to Left.<br>
Did you notice the reference in the game name? If not, watch Game of Thrones you are missing out.<br>

**Instructions:** <br>
Timer starts on press of any key.<br>
Player 1 (orange board surfer): Controls are Up-left-down-right<br>
Player 2 (green cap swimmer): Controls are W-A-S-D respectively (as above)<br>
Press ESC to Pause/Play. If timer hasnt started it stays at 0. But if it has, it runs so that there is no time for strategizing in the middle of playing.

**Game rounds:** <br>
Each time the game is started, multiple rounds (can be modified to some other odd number in the config file, default 5) are played. <br>
In the first round player 1 starts at the bottom and player 2 at the top. This gets swapped in every round to balance difficulty. <br>
The winner of the round faces faster obstacles in the following rounds. The player who wins more rounds (as no. of rounds is odd) is declared the winner.

**Scoring of a round:** <br>
If both players cross over succesfully, the winner is the one who takes less time. <br>
If only one players crosses over succesfully, he wins.<br>
If both players fail to cross then the one with more obstacle score wins. +10 to cross moving obstacle, +5 to cross fixed obstacle, each score is added only once for a particular obstacle.

**Rationale behind scoring:** <br>
Since a player who crosses over gets scores for all obstacles, when both players cross over, accounting for obstacle score seemed redundant to me. So when both cross succesfully, I chose to break the tie only on the basis of time taken (accuracy 0.1 seconds). 
<br>
If only one of the player crosses succesfully, they are the unconditional winner. <br>
If both fail to cross (quite possible given the game's difficulty), the player with more obstacle score is the winner as they did better in that round. <br>
In the rare case of a tie in the tie-break conditions, Player 2 wins. This is because coming top to bottom is very slightly harder and player 2 has to do this for 1 extra round.

**Game difficulty philosophy:** <br>
The game has been kept on the more difficult side to make it challenging and addictive, much like the philosophies followed by games like flappy bird which became viral.

