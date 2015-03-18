#!/usr/bin/python
from sys import argv
from sys import exit
'''
Un parell de anotacions:
	dic_count ens serveir per veure quans cops ens surt un mateix valor
'''
clauses = {}
clauses_all = {}
#TODO: Provar execucio amb tautologia
#TODO: Pensar si nomes utilitzar el maxim
#Aqui pintem les variables que surtem mes i menys
def buildFirstInterpretation(dic_count, interpretation, tmp_inter):
	if len(dic_count) == 0:
		#TODO: Arreglar el print de sortida
		print "SATISTACTIBLE - "
		exit()
	for value in dic_count[1]:
		#TODO: provar si es mes rapid true o 0
		valor = int(value)
		if interpretation[abs(valor)-1] == 5:
			interpretation[abs(valor)-1] = False if valor <=0 else True
			tmp_inter[abs(valor)-1] = interpretation[abs(valor)-1]		
			try:
				del clauses[dic_count[1][value]]
			except KeyError:
				pass
	for i in xrange(len(tmp_inter)):
		if tmp_inter[i] == 5:
			last_key = dic_count.keys()[-1]
			i_str = str(i)
			no_i_str = str(i*-1)
			if i_str in dic_count[last_key]:
				tmp_inter[i] = True
			elif no_i_str in dic_count[last_key]:
				tmp_inter[i] = False 
			else:
				tmp_inter[i] = True
'''
Per llegir les dades del fitxer
'''
def readFile(fname):
	dic = {}
	dic_count = {}
	i = 0
	for line in open(fname, 'r'):
		sp = line.split()
		if sp[0] == 'p':
			n_vars = sp[2]
			n_lines = sp[3]
		elif sp[0] != 'c':
			tmp_dic = {}
			clauses[i] = sp[:-1]
			clauses_all[i] = sp[:-1]
			for var in sp[:-1]:
				value = int(var)
				if value * -1 in tmp_dic:
					del clauses[i]
					break
				tmp_dic[value] = 'X'
			del tmp_dic
			if i != len(clauses):
				for var in sp[:-1]:
					dic[var] = dic[var]+1 if var in dic else 1
					if dic[var] in dic_count:
						dic_count[dic[var]].update({var: 'X'})
					if dic[var]-1 in dic_count:
						del dic_count[dic[var]-1][var] 
					if not dic[var] in dic_count:
						dic_count[dic[var]] = {var: 'X'}
					if dic[var] == 1:
						dic_count[1][var] = i
			else:
				i -= 1

			i += 1
	'''print "clauses: ", clauses
	print "dic: ", dic
	print "dic_count: " ,dic_count'''
	return int(n_vars), dic_count

def work(interpretation):
	i = 0
	while i < 1000:
		i += 1

def test_interpretation_finish(interpretation, tmp_inter):
	i = 0
	for clause in clauses_all:
		for literal in clauses_all[clause]:
			lit = int(literal)
			if (interpretation[abs(lit)-1] == (int(lit)>0)) or (tmp_inter[abs(lit)-1] == (int(lit)>0)): 
				break
			i += 1
		if i == len(clauses_all[clause]):
			return False
		i = 0
	return True

if __name__ == "__main__":
	n_vars, dic_count = readFile(argv[1])
	interpretation = [5]*n_vars
	tmp_inter = interpretation[:]
	buildFirstInterpretation(dic_count, interpretation, tmp_inter)
	print tmp_inter
	work(tmp_inter)
	#print test_interpretation_finish(interpretation, tmp_inter)
	'''print "////clauses: ", clauses
	print "////clauses_all: ", clauses_all
	print "////dic_count: " ,dic_count
	print interpretation
	print tmp_inter'''