#!/usr/bin/env python

def match_choice(c,norm,normI,normT,m,chm,rho,beta):
	
	"""
    Checks match criterion
    Compute choice equation
    Discovers best choice

    :param norm: minimum of input and templates
    :param normI: norm of input
        
    :return: returns category choice location
    """
        
    #m = np.zeros((len(self.IA)*10,1))
	m[c] = norm/normI
	if m[c] < rho:
		chm[c] = 0
	else:
		chm[c] = norm/(beta + normT)

	return chm.argmax(axis=0)
		
def template_options_loop(cmax,chmax,ch,nc,m,chm,rho):
		
	"""
	Match Criterion
		
	:param cmax:	Maximum choice (initialized to be -1)
	:param chmax:	Match Criterion (initialized to be -1)
	:param ch:		Template choice
	:param nc:		Number of Categories	
		
	:return cmax:	Maximum choice template location		
		
	"""

	neg = 0
	while chmax == -1:
		if m[ch] >= rho:
			chmax = chm[ch]
			cmax = ch
		elif neg == nc:
			chmax = 0
		else:
			chm[ch] = -1
			ch = chm.argmax(axis=0)
		neg += 1

	return cmax
		
def ART(I,T,m,chm,nc,min_calc,rho,beta,j):
		
	"""
	Train ART - Create Template Matrix
		
	:param I:		Input
	:param T: 		Template
	:param cmax:	Maximum choice (initialized to be -1)
	:param chmax:	Match Criterion (initialized to be -1)
	"""
	
	for c in range(nc):
		chmax = -1
		cmax = -1
		for i in range(len(I)):
			min_calc[i] = min(I[i,j],T[i,c])
			norm = min_calc.sum()
			normI = I[:,j].sum()
			normT = T[:,c].sum()
			
		ch = match_choice(c,norm,normI,normT,m,chm,rho,beta)
			
	cmax = template_options_loop(cmax,chmax,ch,nc,m,chm,rho)
		
	return cmax,ch