#!/usr/bin/python
from sys import argv
import time
import random

clauses = {}
literals_in_clauses = {}
n_vars = 0
wprob = 0.80
max_tries = 1000
max_flips = 100*425

def read_file(fname):
	global n_vars
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
					for litt in sp[:-1]:
						del literals_in_clauses[litt][key]
					break
				except KeyError:
					try:
						literals_in_clauses[lit]['c'].update({key : True})
					except KeyError:
						literals_in_clauses[lit] = { 'c': {key: True} , 'n':0}

def function_aux(key, interpretation, mode = False):
	for literal in key:
		if mode:
			literals_in_clauses[literal]['n'] = 0
		lit = int(literal)
		if (interpretation[abs(lit)] == (int(lit)>0)) : 
			clauses[key] = True
			return 0
	if mode :
		for literal in key:
			literals_in_clauses[literal]['n'] += 1
	clauses[key] = False
	return 1

def interpretation_correct(interpretation, mode =  False):
	i = 0
	broke = 0
	for clause in clauses:
		broke += function_aux(clause, interpretation, mode)
	return broke

def build_random_interpretation():
	interpretation = {}
	for i in range(n_vars):
		interpretation[i+1] =  bool(random.getrandbits(1))
	return interpretation

def show_result(interpretation):
	print "c Nom solver"
	print "s SATISFIABLE"
	result = ""
	for item in interpretation:
		result += str(item) if interpretation[item] else str(item*-1)
		result += " "
	print "v " + result + "0"

#gsat
def algorithm():
	n_broke = 0
	inside = True
	while 1 :
		inter = build_random_interpretation()
		for _ in xrange(max_flips):
			n_broke = interpretation_correct(inter, True)
			if n_broke == 0:
				show_result(inter)
				return inter
			inter, inside = better_interpretation(inter, n_broke)
			if not inside:
				break
			n_broke = 0


def better_interpretation(inter, n_broke):
	global n_vars, wprob
	inside = False
	best_inte = 0
	first = True
	n_broke = n_vars
	for i in range(n_vars):
		inter[i+1] = False if inter[i+1] else True
		actual_broke = 0
		try:
			for key in literals_in_clauses[str((i+1)*-1)]['c']:
				actual_broke += function_aux(key, inter)
		except KeyError:
			pass
		if actual_broke < n_broke:
			n_broke = actual_broke
			best_inte = i + 1
		inter[i+1] = False if inter[i+1] else True
	prob = random.random()
	if prob < wprob:
		index = random.randint(1,n_vars)
		inter[best_inte] = False if inter[best_inte] else True
	else:
		inter[best_inte] = False if inter[best_inte] else True
	return inter, inside


if __name__ == "__main__":
	read_file(argv[1])
	algorithm()