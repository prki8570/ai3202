# Assignment 2


To run, simply type in python.py Kikkeri_Assignment2.py Worldx (Manhattan/ManhattanSquared), where x = 1 or 2 for the world you choose. You should select which of the Manhattan heuristics as well, for the second argument.

The Manhattan and Manhattan Squared algorithms were influenced by http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html.

This website defines Manhattan as: 

dx = abs(node.x - goal.x)
dy = abs(node.y - goal.y)
return D * (dx + dy)

Thus, Manhattan Squared simply equals (dx+dy)^2.

It is better suited for diagonal traversals of a grid. Diagonals are wiser in our maze too, as a vertical and a horizontal move incur a cost of 14, versus 20 for a horizontal+vertical move.

Sounds great, doesn't it? However, the results speak differently.

For World 1, the Manhattan heuristic incurred a cost of 130 through 12 squares, whereas the cost was 138 with the Manhattan Squared.

For World 2, The Manhattan heuristic had a cost of 144 through 11 squares, and the Manhattan Squared incurred a cost of 152.

The Manhattan Squared uses too many diagonals and does not find the optimal path.

I would stick to the Manhattan heuristic for a problem like this.