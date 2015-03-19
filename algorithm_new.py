#!/usr/bin/python
from sys import argv
import random

clauses = {}
n_vars = 0
n_lines = 0
max_tries = 1
max_flips = 1

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
			i += 1

def function_aux(key, broke , clauses_unsat , interpretation):
	i = 0
	for literal in clauses[key]:
		lit = int(literal)
		if (interpretation[abs(lit)] == (int(lit)>0)) : 
			break
		i += 1
	if i == len(clauses[key]):
		clauses_unsat.append(key)
		broke += 1
	i = 0
	return broke

def interpretation_correct(interpretation):
	i = 0
	broke = 0
	clauses_unsat = []
	for clause in clauses:
		broke = function_aux(clause, broke, clauses_unsat, interpretation)
	return broke, clauses_unsat

def build_random_interpretation():
	interpretation = {}
	for i in range(n_vars):
		interpretation[i+1] =  random.randint(0, 1)
	return interpretation

def show_result(interpretation):
	print "Hem trobat una solucio", interpretation
	pass

#gsat
def algorithm():
	global max_tries, max_flips
	for i in range(max_tries):
		inte = build_random_interpretation()
		for j in range(max_flips):
			n_broke, clauses_unsat = interpretation_correct(inte)
			if n_broke == 0:
				show_result(inte)
				exit()
			inte , go_in= change_better_value(inte, n_broke, clauses_unsat)
			if go_in != True:
				break
	pass

def change_better_value(interpretation, n_broke, clauses_unsat):
	global n_vars
	best_inte = interpretation.copy()
	best_broke = 0
	actual_broke = n_broke
	tmp_int = interpretation.copy()
	go_in = False
	for i in range(n_vars):
		interpretation[i+1] = (interpretation[i+1] + 1) % 2
		for j in range(actual_broke):
			print clauses_unsat
			print j, clauses_unsat[j], n_broke, interpretation
			n_broke = function_aux(clauses_unsat[j], n_broke, [], interpretation)
		if actual_broke > n_broke:
			best_inte = interpretation.best_inte
			best_broke = n_broke
			go_in = True
		interpretation = tmp_int.copy()
	return best_inte, go_in

if __name__ == "__main__":
	read_file(argv[1])
	algorithm()