#!/usr/bin/env python
#++++++++++++++++++++++++++++++++++++++++
# LAPART 1 Test +++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++
# Copyright C. 2017, C. Birk Jones ++++++
#++++++++++++++++++++++++++++++++++++++++

import time
import math
import numpy as np
import pandas as pd
from art import ART

def norm(data,ma,mi):
	tnorm = np.ones((len(data),len(data[0])))
	for i in range(len(data)):
		for j in range(len(data[0])):
			tnorm[i,j] = (data[i,j]-mi[j])/(ma[j] - mi[j])
	return tnorm
    
def dnorm(data,ma,mi):
    dnorm = np.ones((len(data),len(data[0])))
    for i in range(len(data)):
        for j in range(len(data[0])):
            dnorm[i,j] = (data[i,j]*(ma[j]-mi[j]))+mi[j]
    return dnorm

class test:

	def __init__(self,xA,TA,TB,L,rhoA,rhoB,beta,alpha,nep,memory_folder):
	
		# Parameters
		self.rhoA = rhoA
		self.rhoB = rhoB
		self.beta = beta
		self.alpha = alpha
		self.nep = nep
		
		self.folder = memory_folder
		
		''' Min and Max of Input Data '''
		maxminA = pd.read_csv('%s/maxminA.csv'%self.folder).values
		past_maxA,past_minA = maxminA[:,1:2],maxminA[:,2:3]
		
		if len(xA) > 1:
			current_maxA,current_minA = np.array([xA.max(axis=0)]).T,np.array([xA.min(axis=0)]).T
		else:
			current_maxA,current_minA = xA.T,xA.T
		
		mmA = np.hstack([past_maxA,current_maxA,past_minA,current_minA]).T	
		self.maxA,self.minA = np.array([mmA.max(axis=0)]).T,np.array([mmA.min(axis=0)]).T
		
		maxminB = pd.read_csv('%s/maxminB.csv'%self.folder).values
		self.maxB,self.minB = maxminB[:,1:2],maxminB[:,2:3]
		
		''' Normalize Input Data '''
		self.xAn = norm(xA,self.maxA,self.minA)
		
		''' Complement Code Data '''
		self.IA = np.transpose(np.hstack([self.xAn, 1-self.xAn]))
				
		''' Number of Inputs '''
		self.nAB = len(self.IA[0])
		
		self.TA = np.transpose(TA)
		self.TB = np.transpose(TB)
		self.L = L	
		self.ncA = len(TA)
		
		self.minAm = np.ones((len(xA[0])*2,1))
		self.chAm = np.zeros((len(TA)*10,1))
		self.mA = np.zeros((len(TA)*10,1))
		
		self.CA = np.zeros((len(xA)*2,1))
		self.CB = np.zeros((len(xA)*2,1))
		self.TBt = np.zeros((len(xA)*2,len(self.TB)))

		
	def lapart_test(self,xA):
	
		for ep in range(self.nep):

			for j in range(0,self.nAB):

				''' Present Inputs to A Side Templates '''
				cmax,ch = ART(self.IA,self.TA,self.mA,self.chAm,self.ncA,self.minAm,self.rhoA,self.beta,j)
				
				if cmax == -1:
					''' A Templates do not resonate '''
					self.CA[j] = -1
				else:
					''' A Templates do resonate '''
					self.CA[j] = ch
					
				for i in range(len(self.L[0])):
					#print self.L[ch,i]
					if self.L[ch,i] == 1:
						if cmax == -1:
							self.CB[j] = cmax
							self.TBt[j] = self.TB[:,i]	#np.ones((1,len(xA[0]))) 
							
						else:
							self.CB[j] = i
							self.TBt[j] = self.TB[:,i]
							
						break
						
			
		TB = self.TBt[:len(xA)]
		
		TBnl,TBnr = np.zeros((len(TB),1)),np.zeros((len(TB),1))
		for i in range(len(TB[0])):
			if i == len(TB[0])/2:
				TBn = dnorm(1-np.array([TB[:,i]]).T,self.maxB,self.minB)
				TBnr = np.append(TBnr,TBn,1)	
			else:
				TBn = dnorm(np.array([TB[:,i]]).T,self.maxB,self.minB)	
				TBnl = np.append(TBnl,TBn,1)

		TBn = np.hstack([TBnl[:,1:],TBnr[:,1:]])
		
		return self.CA[:len(xA),:],self.CB[:len(xA),:],TB,TBn,self.IA[:len(xA[0]),:].T


def lapArt_test(xA,rhoA=0.9,rhoB=0.9,beta=0.000001,alpha=1.0,nep=1,memory_folder=''):

	"""
	Test LAPART Algorithm
	
	:param xA:		A-Side Input Matrix (float)
	:param rhoA:	A-Side free parameter (float)
	:param rhoB:	B-Side free parameter (float)
	:param beta:	Learning rate free parameter (float)
	:param alpha:	Choice Parameter (float)
	:param nep:		Number of epochs (integer)
	:param memory_folder:	Folder to store memory (string)
	
	:return CB:	B-Side categories vector (float)
	:return TB:	B-Side template matrix (float)
	:return TBn: B-Side normalized template matrix (float)
	:return df: Pandas dataframe - A & B categories, A-Side inputs
	:return elapsed_time: Seconds to complete training (float) 
	"""

	start_time = time.time()

	TA,TB = pd.read_csv('%s/TA.csv'%memory_folder).values,pd.read_csv('%s/TB.csv'%memory_folder).values
	L = pd.read_csv('%s/L.csv'%memory_folder).values
	TA,TB,L = TA[:,1:],TB[:,1:],L[:,1:]
	
	print(xA)
	
	ann = test(xA,TA,TB,L,rhoA,rhoB,beta,alpha,nep,memory_folder)
	CA,CB,TB,TBn,IA = ann.lapart_test(xA)
	df = pd.DataFrame(np.hstack([CA,CB,IA]))
	df = df.rename(columns={0: 'CA', 1: 'CB'})
	
	elapsed_time = time.time() - start_time
	
	return CB,TB,TBn,df,elapsed_time