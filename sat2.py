from sys import argv
import random

def solve(num_vars, clauses, maxflips, wprob):
    RndInterpretationGenerator = randomInterpretation   
    InitializeClausesData = initializeClausesData
    ChoseAndFlipVar = choseAndFlipVar
    
    num_clauses = len(clauses)
    var_range = xrange(1, num_vars+1)
    flip_range = xrange(maxflips)
    litclauses = classifyClausesByVariable(num_vars, clauses)
    
    csatlits = { c: 0 for c in clauses }
      
    while True:
        rintp = RndInterpretationGenerator(num_vars)
        num_satclauses = InitializeClausesData(clauses, rintp, csatlits)     
        
        if num_satclauses == num_clauses:
            return rintp
        
        for i in flip_range:
            prob = random.random()
                        
            if prob < wprob:
                num_satclauses = randomWalk(clauses, litclauses, rintp,
                                            csatlits, num_satclauses)
                                            
            else:
                num_satclauses = ChoseAndFlipVar(litclauses, rintp, csatlits, 
                                                 num_satclauses, var_range)

            if num_satclauses == num_clauses:
                return rintp                  
            
#
#
def randomWalk(clauses, litclauses, rintp, csatlits, num_satclauses):
    
    var = 0    
    
    for c in clauses:
        if csatlits[c] == 0:
            var = abs(random.sample(c,1)[0])
            break
            
    rintp[var] = not rintp[var]

    for c in litclauses[var]:
        satlits = csatlits[c]
        if not satlits:
            num_satclauses += 1
            satlits = 1
        elif satlits == 1:
            lit = var if rintp[var] else -var
            if lit in c:
                satlits = 2
            else:
                satlits = 0
                num_satclauses -= 1
        else:
            lit = var if rintp[var] else -var
            if lit in c:
                satlits += 1
            else:
                satlits -= 1
        
        csatlits[c] = satlits

    return num_satclauses

def choseAndFlipVar(litclauses, rintp, csatlits, old_num_satclauses, var_range):
    best_result = -1
    chosed_var = 0
    
    for i in var_range:
        num_sat_change = satClausesOnIntpChange(litclauses[i], rintp, csatlits, old_num_satclauses, i)
        if num_sat_change > best_result:
            best_result = num_sat_change
            chosed_var = i
    
    flipVar(litclauses[chosed_var], rintp, csatlits, chosed_var)
    
    return best_result            

#
#
def randomInterpretation(num_vars):
    l = [None]
    l.extend([ random.choice( (True, False) ) for i in xrange(num_vars) ])
    return l
            
#
#
def initializeClausesData(clauses, intp, csatlits):
    num_sat_clauses = 0    
    
    for c in clauses:
        num_sat_lits = 0        
        
        for lit in c:
            if intp[lit] if lit > 0 else not intp[-lit]:
                num_sat_lits += 1
                
        csatlits[c] = num_sat_lits
                    
        # If it is different from zero
        if num_sat_lits:
            num_sat_clauses += 1    
            
    return num_sat_clauses

def classifyClausesByVariable(num_vars, clauses):
    
    litclauses = [set() for _ in xrange(num_vars+1)]
    
    for clause in clauses:
        for l in clause:
            alit = abs(l)
            litclauses[alit].add(clause)
            
    return litclauses

def read_file(fname):
    n_vars = 0
    #clauses = 
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
                        del literals_in_clauses[str(int(litt))][key]
                    break
                except KeyError:
                    try:
                        literals_in_clauses[str(abs(int(lit)))]['c'].update({key : True})
                    except KeyError:
                        literals_in_clauses[str(abs(int(lit)))] = { 'c': {key: True} , 'n':0}
    return clauses, n_vars

def parseCNF(fname):
    num_vars = 0
    clauses = set()

    cnf_file = open(fname, 'r')    
    
    try:
        for nline, line in enumerate(cnf_file):
            lvalues = line.strip().split()
            
            if not lvalues or lvalues[0] == 'c':
                continue
            
            elif lvalues[0] == 'p':
                if lvalues[1] != 'cnf':
                    raise SyntaxError('Invalid format identifier "%s".'
                                % ( lvalues[1]) )
                             
                num_vars = int(lvalues[2])
                #num_clauses = int(lvalues[3])                
                
            else:
                values = map(int, lvalues)                    
                clause = set()
                
                for lit in values:
                    if lit == 0:
                        if clause not in clauses:                        
                        
                            clause = frozenset(clause)
                            clauses.add( clause )

                        clause = None # Check line ends with 0
                        
                    else:
                        clause.add(lit)

                        if lit < -num_vars or lit > num_vars:
                            raise SyntaxError('Invalid literal %d '
                                ', it must be in range [1, %d].'
                                % (lit, num_vars) )

                if clause:
                    raise SyntaxError('Not found the trailing 0')
                
    except SyntaxError, e:
        sys.stderr.write('Error parsing file "%s" (%d): %s\n' % 
                                    (fname, nline, str(e)) )
        raise e
            
    return num_vars, clauses

def satClausesOnIntpChange(varclauses, rintp, csatlits, num_satclauses, var):
    """
    Counts the number of satisfied clauses after flipping the value of 'var'
    """
    rintp[var] = not rintp[var]
    
    for c in varclauses:
        satlits = csatlits[c]
        
        # If num sat lits was 0 with the flip it must be 1
        # so the clause is satisfied with the change
        if satlits == 0:
            num_satclauses += 1
        
        # If the var is falsified it meas it was the only satisfied literal
        # with the previous interpretation
        elif satlits == 1:
            lit = var if rintp[var] else -var
            if not lit in c:
                num_satclauses -= 1    
    
    rintp[var] = not rintp[var]
    
    return num_satclauses

def flipVar(varclauses, rintp, csatlits, chosed_var):
    rintp[chosed_var] = not rintp[chosed_var]
    lit = chosed_var if rintp[chosed_var] else -chosed_var    
    
    for c in varclauses:
        if lit in c:
            csatlits[c] += 1
        else:
            csatlits[c] -= 1

if __name__ == "__main__":
    num_vars, clauses =  parseCNF(argv[1])#read_file(argv[1])
    print solve(num_vars, clauses, len(clauses)//2, 0.35)