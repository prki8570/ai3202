# CSCI 3202 Assignment 6
# Pradyumna Kikkeri
# Collaborated with Nikolai Tangdit
# Due Wednesday, October 28, 2015 :(


#old useless s**t-code
'''class Node(object):
	def __init__(self, name, probabilityDistribution):
		self.name = name
		self.probabilityDistribution probabilityDistribution
		self.edge = None
		self.parent = None

def variableInit():
	Pollution = Node("Pollution", {"low": 0.9})
	Cancer = Node("Cancer", {"low":{"T": 0.03, "F": 0.001}, "high":{"T": 0.05, "F":0.02}})
	Smoker = Node("Smoker", {"T": 0.3})
	Dyspnoea = Node("Dyspnoea", {"T": 0.65, "F": 0.35})
	Xray = Node("Xray", {"T": 0.9, "F": 0.2})
	Pollution.edge = Cancer
	Smoker.edge = Cancer
	Cancer.edge = [Xray, Dyspnoea]
	Cancer.parent = [Pollution, Smoker]'''

import getopt, sys

#Make a node
class Node(object):
	def __init__(self, name):
		self.name = name
		self.prior = 0.0
		self.probDist = None
		self.parent = None
		self.edge= []
# Initialize the Baye's net
# Bae's Net lololol
class BayesNet(object):

	def __init__(self):
		self.data = []
#initialize
	def NetInit(self):
		P = Node('P')
		P.prior = 0.9
		S = Node('S')
		S.prior = 0.3
		C= Node('C')
		C.parent = [P, S]
		P.edge = [C]
		S.edge = [C]
		C.probDist= {"low": {"T": 0.03, "F": 0.001}, "high": {"T":0.05, "F": 0.02}}
		X = Node('X')
		X.parent= [C]
		X.probDist= {"T": 0.9, "F": 0.2}
		D= Node('D')
		D.parent= [C]
		C.edge= [X,D]
		D.probDist= {"T": 0.65, "F": 0.30}
		self.data= [P,S,C,X,D]

	# Calculation of marginal probability works.
	def marginal(self, node):
		if node.name is 'P':
			return node.prior
		elif node.name is 'S':
			return 1- node.prior
		elif node.name is 'C':
			marg= (node.parent[1].prior)*node.probDist["high"]["T"]+(1-node.parent[1].prior)*node.probDist["high"]["F"]
			#P(s)*P(c|~p,s) + P(~s)*P(c|~p, ~s)
			marg *= (1-node.parent[0].prior)
			#Becomes P(~p)P(s)P(c|~p,s) + P(~p)P(~s)P(c|~p,~s)
			marg += (node.parent[0].prior)*((node.parent[1].prior)*node.probDist["low"]["T"]+(1-node.parent[1].prior)*node.probDist["low"]["F"])
			#P(~p)P(s)P(c|~p,s) + P(~p)P(~s)P(c|~p,~s) + P(p)P(s)P(c|p,s) + P(p)P(~s)P(c|p,~s)
			return marg
		elif node.name is 'X' or 'D':
			cancer_marg1=  node.parent[0].parent[1].prior * node.parent[0].probDist["high"]["T"]+ (1- node.parent[0].parent[1].prior)*node.parent[0].probDist["high"]["F"]
			cancer_marg1 *= (1- node.parent[0].parent[0].prior)
			cancer_marg2 = node.parent[0].parent[1].prior * node.parent[0].probDist["low"]["T"]+ (1- node.parent[0].parent[1].prior)*node.parent[0].probDist["low"]["F"]
			cancer_marg2 *= node.parent[0].parent[0].prior
			cancer_marg = cancer_marg1 + cancer_marg2
			#Now have cancer's marginal
			marg= cancer_marg* node.probDist["T"] + (1 - cancer_marg)* node.probDist["F"]
			return marg

	def findNode(name):
		for node in self.data:
			if node.name is name:
				return node
		#failed to find the name
		print "Node non-existent."
	
	
		

	# Adjust the prior of P or S and set it to newPrior
	def adjPrior(self, rv, newPrior):
		if rv.name is not 'P' or 'S':
			return
		else:
			rv.prior= newPrior
			print "New prior is now", newPrior


# Parser based on Prof. Hoenigman's	
def getoptParser(opts, args):

    for o, a in opts:
		if o in ("-p"):
			print "flag", o
			print "args", a
			print a[0]
			print float(a[1:])
			#setting the prior here works if the Bayes net is already built
			#print BN.adjPrior(a[0], float(a[1:]))
		elif o in ("-m"):
			print "flag", o
			print "args", a
			print (type(a))
			print BN.marginal(BN.findNode(a))
		elif o in ("-g"):
			print "flag", o
			print "args", a
			print type(a)
			'''you may want to parse a here and pass the left of |
			and right of | as arguments to calcConditional
			'''
			p = a.find("|")
			print a[:p]
			print a[p+1:]
			#calcConditional(a[:p], a[p+1:])
		elif o in ("-j"):
			print "flag", o
			print "args", a
		else:
			assert False, "unhandled option"






BN = BayesNet()
BN.NetInit()
	
try:
	opts, args = getopt.getopt(sys.argv[1:], 'g:j:m:p:')
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)
getoptParser(opts, args)