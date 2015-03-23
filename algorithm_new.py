#!/usr/bin/python
from sys import argv
import random

clauses = {}
literals_in_clauses = {}
n_vars = 0
n_lines = 0
max_tries = 1000
max_flips = 1000

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
		interpretation[i+1] =  bool(random.getrandbits(1))
	return interpretation

def show_result(interpretation):
	print "Hem trobat una solucio", interpretation

#gsat
def algorithm():
    n_broke = 0
    inside = True
    for _ in xrange(max_tries):
        inter = build_random_interpretation()
        for x in xrange(max_flips):

            print x
            n_broke = interpretation_correct(inter)
            if n_broke == 0:
                show_result(inter)
                return inter
            inter, inside = better_interpretation(inter, n_broke)
            if not inside:
                break
            n_broke = 0


def better_interpretation(inter, n_broke):
    global n_vars
    inside = False
    set = []
    for i in range(n_vars):
        inter[i+1] = False if inter[i+1] else True
        if n_broke > interpretation_correct(inter):
            set.append(i+1)
            inside = True
        inter[i+1] = False if inter[i+1] else True
    if inside:
        var = set[random.randint(0,len(set)-1)]
        inter[var] = False if inter[var] else True
    return inter, inside
	#print interpretation
	#intepretation = {1: 0, 2: 1, 3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 0, 9: 1, 10: 1, 11: 0, 12: 1, 13: 1, 14: 1, 15: 0, 16: 1, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 1, 25: 1, 26: 0, 27: 1, 28: 0, 29: 0, 30: 0}


if __name__ == "__main__":
	read_file(argv[1])
	algorithm()
