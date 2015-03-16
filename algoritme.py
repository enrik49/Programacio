#!/usr/bin/python
from sys import argv
'''
Un parell de anotacions:
	dic_count ens serveir per veure quans cops ens surt un mateix valor
	clauses on tenim les clausules de moment esta en llista pero es pot canviar a diccionari
'''

#Aqui pintem les variables que surtem mes i menys
def buildFirstInterpretation(dic_count, interpretation):
	for value in dic_count[1]:
		valor = int(value)
		interpretation[abs(valor)] = True if valor <=0 else False
	for value in dic_count[len(dic_count)]:
		print value
	print interpretation
'''
Per llegir les dades del fitxer
'''
def readFile(fname):
	dic = {}
	dic_count = {}
	clauses = []
	for line in open(fname, 'r'):
		sp = line.split()
		if sp[0] == 'p':
			n_vars = sp[2]
			n_lines = sp[3]
		elif sp[0] != 'c':
			clauses.append(sp[:-1])
			for var in sp[:-1]:
				dic[var] = dic[var]+1 if var in dic else 1
				if dic[var] in dic_count:
					dic_count[dic[var]].update({var: 'X'})
				if dic[var]-1 in dic_count:
					del dic_count[dic[var]-1][var] 
				if not dic[var] in dic_count:
					dic_count[dic[var]] = {var: 'X'}
	print "clauses: ", clauses
	print "dic: ", dic
	print "dic_count: " ,dic_count
	return int(n_vars), dic_count

if __name__ == "__main__":
	n_vars, dic_count = readFile(argv[1])
	interpretation = {}
	buildFirstInterpretation(dic_count, interpretation)