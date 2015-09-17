import math
import sys


#Pradyumna Kikkeri 101417122
#CSCI 3202 Hoenigman
#Fall 2015
#Due Friday, September 18, 2015, 4:00 PM


class Node(object): #spec'd per Prof. Hoenigmann's outline in the PDF

	def __init__(self, horiz_space, vert_space):
		self.i = horiz_space
		self.j = vert_space
		self.distanceToStart = 0
		self.heuristic = None
		self.f = None
		self.parentNode = None

	def eq (self, misc):
		return (self.i == misc.i and self.j == misc.j)

	def heuristicSetup(self, parentNode, v, heuristic_choice):
		self.parentNode = parentNode

		distance_from_parent = abs(parentNode.i - self. i) + abs(parentNode.j - self.j)
		if(distance_from_parent == 2): # diagonal
			self.distanceToStart = parentNode.distanceToStart + 14
		elif(distance_from_parent == 1): # horizontal/vertical
			self.distanceToStart = parentNode.distanceToStart + 10
# algorithms from http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
		if (v == 1):
			self.distanceToStart += 10
		if (heuristic_choice == 'MNH'):
			self.heuristic = abs(9 - self.i) + abs(7 - self.j) # Manhattan
		else:
			self.heuristic = (abs(9 - self.j*10) + abs(7-self.i*10)) ** 2 #Manhattan Squared
		self.f = self.distanceToStart + self.heuristic

	def cmp(self, tParent, v):
		distance_from_parent = abs(tParent.i - self.i) + abs(tParent.j-self.j)
		tDist = 0
		if(distance_from_parent == 2):
			tDist = tParent.distanceToStart + 14 #diagonal
		elif(distance_from_parent == 1):
			tDist = tParent.distanceToStart + 10
		if(v == 1):
			tDist += 10
		if(tDist < self.distanceToStart):
			self.distanceToStart = tDist
			self.parentNode = tParent
			self.f = self.distanceToStart + self.heuristic


def A_star_search(mat, heuristic):
	
	start_point = Node(0,0)
	queue_open = []
	cl = [Node(-1, -1)]
	queue_open.append(start_point)
	iterator = 0
	while(not cl[-1].eq(Node(9,7)) and len(queue_open) > 0):
		queue_open.sort( key = lambda x: x.f)
		op = queue_open[0]
		queue_open.remove(op)
		cl.append(op)
		for i in range(-1,2):
			for j in range(-1,2):
				x_value = op.i + i
				y_value = op.j + j
				if(x_value >= 0 and x_value <= 9 and y_value >= 0 and y_value <= 7):
					iterator += 1
					new = Node(x_value, y_value)
					boot = True
					for b in cl:
						if b.eq(new):
							boot = False


					if(mat[x_value][7-y_value] is not 2 and boot):

						newn = Node(x_value, y_value)
						boo = True
						for u in queue_open:
							if u.eq(newn):
								boo = False



						if boo:
							queue_open.append(new)
							new.heuristicSetup(op, mat[x_value][7-y_value], heuristic)
						else:
							new.cmp(op, mat[x_value][7-y_value])

	k = cl[-1]
	print('Distance:', k.distanceToStart, 'Iterated through:', iterator)
	last = []
	while(k!=None):
		last.insert(0, k)
		k = k.parentNode
	for c in last:
		print(c.i, c.j)

if __name__ == '__main__':
	if(len(sys.argv) != 3):
		print("Pass in the world number and chosen heuristic.")
		sys.exit(0)
	world_file = ''
	heuristic = ''
	if(sys.argv[1] == "World1" or sys.argv[1] == "world1"):
		world_file = 'World1.txt'
	elif(sys.argv[1] == "World2" or sys.argv[1] == "world2"):
		world_file = 'World2.txt'

	else:
		print("That world does not exist.")
		sys.exit(0)
	if(sys.argv[2] == "Manhattan" or sys.argv[2] == "manhattan"):
		heuristic = 'MNH'
	else:
		heuristic = 'diag'

	board = [[], [], [], [], [], [], [], [], [], []]

	with open(world_file) as wfile:
		for line in wfile:
			for x, y in enumerate(line.split()):
				board[x].append(int(y))

	A_star_search(board, heuristic)