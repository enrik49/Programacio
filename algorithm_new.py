#!/usr/bin/python
from sys import argv
import random

clauses = {}
literals_in_clauses = {}
n_vars = 0
n_lines = 0
max_tries = 1000
max_flips = 50

def read_file(fname):
	global n_vars
	global n_lines
	i = 0
	for line in open(fname, 'r'):
		sp = line.split()
		if sp[0] == 'p':
			n_vars = int(sp[2])
			n_lines = int(sp[3])
		elif sp[0] != 'c':
			clauses[i] = sp[:-1]
			for lit in clauses[i]:
				try:
					literals_in_clauses[str(int(lit)*-1)][i]
					del clauses[i]
					del literals_in_clauses[str(int(lit)*-1)][i]					
					break
				except KeyError:
					if lit in literals_in_clauses:
						literals_in_clauses[lit].update({i : 'X'})
					else:
						literals_in_clauses[lit] = {i: 'X'}

			i += 1

def function_aux(key, interpretation):
	i = 0
	for literal in clauses[key]:
		lit = int(literal)
		if (interpretation[abs(lit)] == (int(lit)>0)) : 
			break
		i += 1
	if i == len(clauses[key]):
		return 1
	return 0

def interpretation_correct(interpretation):
	i = 0
	broke = 0
	for clause in clauses:
		broke += function_aux(clause, interpretation)
	return broke

def build_random_interpretation():
	interpretation = {}
	for i in range(n_vars):
		interpretation[i+1] =  random.randint(0, 1)
	return interpretation

def show_result(interpretation):
	print "Hem trobat una solucio", interpretation

#wsat
def algorithm():
	global max_tries, max_flips
	for i in xrange(max_tries):
        	print i
		inte = build_random_interpretation()
		for _ in xrange(max_flips):
			n_broke = interpretation_correct(inte)
			#print inte
			print n_broke
			if n_broke == 0:
				show_result(inte)
				exit()
			inte, go_in= change_better_value(inte, n_broke)
			if not go_in:
				print "break"
				break

def change_better_value(interpretation, actual_broke):
	global n_vars
	best_inte = interpretation.copy()
	best_broke = 0
	n_broke = 0
	tmp_int = interpretation.copy()
	go_in = False
	for i in range(n_vars):
		interpretation[i+1] = (interpretation[i+1] + 1) % 2
		try:
			for j in literals_in_clauses[str(i+1)]:
				#print "lite", literals_in_clauses[str(value)]
				#print "j", j, "n_broke", n_broke, "inter", interpretation
				#print function_aux(j, interpretation)
				n_broke += function_aux(j, interpretation)
				#print n_broke, j
			for j in literals_in_clauses[str((i+1)*-1)]:
				n_broke += function_aux(j, interpretation)
		except KeyError:
			pass
		if actual_broke > n_broke:
			actual_broke = n_broke
			best_inte = interpretation.copy()
			best_broke = n_broke
			go_in = True
		interpretation[i+1] = (interpretation[i+1] + 1) % 2
		n_broke = 0
	return best_inte, go_in

if __name__ == "__main__":
	read_file(argv[1])
	#print "cla", clauses
	#print "lit", literals_in_clauses
	algorithm()
