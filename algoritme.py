#!/usr/bin/python
from sys import argv

dic = {}
dic_count = {}
clauses = []
for line in open(argv[1], 'r'):
	sp = line.split()
	if sp[0] == 'p':
		n_vars = sp[2]
		n_lines = sp[3]
	elif sp[0] != 'c':
		clauses.append(sp[:-1])
		for var in sp[:-1]:
			dic[var] = dic[var]+1 if var in dic else 1
			if dic[var] in dic_count:
				dic_count[dic[var]].update({var:'X'})
				
				if dic[var] != 1:
					del dic_count[dic[var]][var]
			else:
				dic_count[dic[var]] = {var:'X'}

				if dic[var] != 1:
					del dic_count[dic[var]][var]
print "dic -- " , dic
print "dic_count -- ",dic_count
