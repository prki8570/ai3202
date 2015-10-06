import sys
import math

# Pradyumna Kikkeri, 101417122, CSCI 3202 Fall 2015


gamma = 0.9 # as described in handout
up = "up"
down = "down"
left = "left"
right = "right"
nil = "x"
dest = "DD"
all_possible_moves = [up, down, left, right, nil, dest]

class Node(object):
	def __init__(self, position, value_of_space):
		self.post = position
		self.val = value_of_space

		if (value_of_space == 0 or value_of_space == 2): # empty space or hit a wall, respectively
			self.reward = 0
		elif (value_of_space == 1): #for a mountain
			self.reward = -1
		elif (value_of_space == 3): #snake!
			self.reward = -2
		elif (value_of_space == 4): #a barn
			self.reward = 1

		if (value_of_space == 50): #end
			self.dir = dest
			self.utility = 50
		else:
			self.dir = nil
			self.utility = 0

	def getDirection(self):
		return self.dir
	def setUtility(self, newUtility):
		self.utility = newUtility
	def setDirection(self, newDirection):
		self.dir = newDirection
	def getUtility(self):
		return self.utility
	def getReward(self):
		return self.reward
	def getValue(self):
		return self.val
	def getLocation(self):
		return self.post
	def __str__(self):
		return ("Position in world: " + str(self.post) + ", Next move: " + self.dir + ", Utility: " + str(self.utility))

def Grapher(file):
	fp = open(file, 'r').readlines()
	graph = []
	for line in reversed(fp):
		graph.append(line.split(" "))

	graph = graph[1:]
	list_of_nodes = []

	for i in range(len(graph)):
		list_of_nodes.append([])
		for j in range(len(graph[i])):
			list_of_nodes[i].append(Node((j, i), int(graph[i][j])))

	return list_of_nodes

def UtilityCalculator(world, node):
	if node.getValue() == 2 or node.getValue() == 50:
		return

	location = node.getLocation()
	y = location[1]
	x = location[0]

	if y - 1 < 0:
		downutility = 0
	else:
		downutility = world[y-1][x].getUtility()
	if x - 1 < 0:
		leftutility = 0
	else:
		leftutility = world[y][x-1].getUtility()
	if y + 1 > 7:
		uputility = 0
	else:
		uputility = world[y+1][x].getUtility()
	if x + 1 > 9:
		rightutility = 0
	else:
		rightutility = world[y][x+1].getUtility()
# calculation of utilities as described in MDP
	down_t = .8 * downutility + .1 * leftutility + .1 * rightutility
	up_t = .8 * uputility + .1 * leftutility + .1 * rightutility
	left_t = .8 * leftutility + .1 * uputility + .1 * downutility
	right_t = .8 * rightutility + .1 * uputility + .1 * downutility

	best = []
	best.append((down_t, down))
	best.append((up_t, up))
	best.append((left_t, left))
	best.append((right_t, right))
	best_max = max(best)

	temp = node.getUtility()

	node.setUtility(float(node.getReward() + gamma * best_max[0]))
	node.setDirection(best_max[1])

	return abs(temp - node.getUtility())

def pathprinter(world):
	print("\nHere is your list of moves to traverse an optimal path for the world you have\n inputted.\n")
	x = 0
	y = 0
	node = world[y][x]
	while node.getDirection() != "DD":
		print node
		if node.getDirection() == up:
			y+= 1
		elif node.getDirection() == down:
			y-= 1
		elif node.getDirection() == left:
			x-= 1
		elif node.getDirection() == right:
			x+= 1
		node = world[y][x]

def pathfinder(world, eps):
	delta = float("inf")
	while not (delta < eps * (1-gamma) / gamma):
		delta = 0
		for row in reversed(world):
			for i in reversed(row):
				newDelta = UtilityCalculator(world, i)
				if newDelta > delta:
					delta = newDelta

	pathprinter(world)

if __name__ == '__main__':
	if(len(sys.argv) != 3):
		print("Make sure you put in arguments for the world filename and epsilon value.")
		sys.exit(0)
	fp = ""
	if (sys.argv[1] == "World1MDP.txt"):
		fp = "World1MDP.txt"
	else:
		print("World not found.")
		sys.exit(0)
	p = sys.argv[2]
	try:
		p = float(p)
	except ValueError:
		print("Need a float as epsilon value.")
		sys.exit(0)
	m = Grapher(fp)
	sun = pathfinder(m, p)