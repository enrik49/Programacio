#!/usr/bin/python
from sys import argv
import random

clauses = {}
literals_in_clauses = {}
wprob = 0.35
lit_unsat = {}
n_vars = 0

def read_file(fname):
	global n_vars
	enter =  False
	for line in open(fname, 'r'):
		sp = line.split()
		if sp[0] == 'p':
			n_vars = int(sp[2])
		elif sp[0] != 'c':
			key = tuple(sorted(sp[:-1]))
			clauses[key] =  False
			for lit in sp[:-1]:
				try:
					literals_in_clauses[str(int(lit)*-1)][key]
					del clauses[key]
					enter = True
					break
				except KeyError:
					try:
						literals_in_clauses[lit].update({key : True})
					except KeyError:
						literals_in_clauses[lit] = { key: True }
			if enter:
				try:
					for litt in sp[:-1]:
						del literals_in_clauses[litt][key]
				except KeyError:
					pass
			enter =  False

def function_aux(key, interpretation, mode = True):
	for literal in key:
		lit = int(literal)
		if (interpretation[abs(lit)] == (int(lit)>0)) : 
			return 0
	if mode:
		for lit in key:
			try:
				lit_unsat[lit] += 1
			except KeyError:
				lit_unsat[lit] = 1
	return 1

def interpretation_correct(interpretation):
	i = 0
	broke = 0
	lit_unsat = {}
	for clause in clauses:
		broke += function_aux(clause, interpretation)
	return broke

def build_random_interpretation():
	interpretation = {}
	for i in range(n_vars):
		interpretation[i+1] =  bool(random.getrandbits(1))
	return interpretation

def show_result(interpretation):
	print "c Law y orden"
	print "s SATISFIABLE"
	result = ""
	for item in interpretation:
		result += str(item) if interpretation[item] else str(item*-1)
		result += " "
	print "v " + result + "0"

def choseAndFlipVar(rinter):
	n_broke = 0
	best_value = 0
	best_inter = -1
	for lit in lit_unsat:
		position = abs(int(lit))
		rinter[position] = not rinter[position]
		oposite = str(int(lit)*-1)
		try:
			for key in literals_in_clauses[oposite]:
				n_broke += function_aux(key, rinter,False)
		except KeyError:
			pass
		if (lit_unsat[lit] - n_broke) > best_value:
			best_value = lit_unsat[lit] - n_broke
			best_inter = position
		rinter[position] = not rinter[position]
		n_broke = 0
	if best_inter != -1:
		rinter[best_inter] = not rinter[best_inter]
	return rinter

def solve():
	global n_vars, wprob
	while True:
		rinter = build_random_interpretation()
		for _ in xrange(n_vars*2):
			broke = interpretation_correct(rinter)
			if broke == 0 : 
				show_result(rinter)
				exit()
			prob = random.random()        
			if prob < wprob:
				position = random.randint(1,n_vars)
				rinter[position] = not rinter[position]
			else:
				rinter = choseAndFlipVar(rinter)

if __name__ == "__main__":
	read_file(argv[1])
	solve()
	'''exit()
	rinter = build_random_interpretation()
	rinter = {1: True, 2: True, 3: True, 4: True}
	broke = interpretation_correct(rinter)
	print "Clauses:\n",clauses
	print "Literals in clauses:"
	for key in literals_in_clauses:
		print key,":",literals_in_clauses[key]
	print "interpretation random:\n", rinter
	print "Number broke: ", broke, ", len:", len(clauses)
	print "Lit unsat:\n", lit_unsat
	rinter = choseAndFlipVar(rinter)
	broke = interpretation_correct(rinter)
	print "Number broke: ", broke, ", len:", len(clauses)
	show_result(rinter)'''

