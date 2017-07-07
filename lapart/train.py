#!/usr/bin/env python
#++++++++++++++++++++++++++++++++++++++++
# LAPART 1 Train ++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++
# Copyright C. 2017, C. Birk Jones ++++++
#++++++++++++++++++++++++++++++++++++++++

import time
import math
import numpy as np
import pandas as pd
from art import ART

def norm(data,ma,mi):

	"""
    
    Parameters
    ----------
    data : matrix
    ma : maxtrix
    """ 

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

class train:

	def __init__(self,xA,xB,rhoA,rhoB,beta,alpha,nep,TA,TB,L,memory_folder,update_templates):
	
		''' Update Existing Templates '''
		self.update = update_templates
		self.folder = memory_folder
	
		''' LAPART Parameters '''
		self.rhoA = rhoA
		self.rhoB = rhoB
		self.beta = beta
		self.alpha = alpha
		self.nep = nep
		
		''' Min and Max of Input Data '''
		if self.update == False:
			self.maxA,self.minA = np.array([xA.max(axis=0)]).T,np.array([xA.min(axis=0)]).T
			self.maxB,self.minB = np.array([xB.max(axis=0)]).T,np.array([xB.min(axis=0)]).T
			
			self.maxA = self.maxA #+ self.maxA * 0.3 
			self.maxB = self.maxB #+ self.maxB * 0.3
			
			self.minA = self.minA 
			self.minB = self.minB 
			
			mA,mB = np.hstack([self.maxA,self.minA]),np.hstack([self.maxB,self.minB])
			dfmA,dfmB = pd.DataFrame(mA,columns=[['max','min']]),pd.DataFrame(mB,columns=[['max','min']])
			dfmA.to_csv('%s/maxminA.csv'%self.folder)
			dfmB.to_csv('%s/maxminB.csv'%self.folder)
		else:
			maxminA = pd.read_csv('%s/maxminA.csv'%self.folder).as_matrix()
			maxminB = pd.read_csv('%s/maxminB.csv'%self.folder).as_matrix()
			past_maxA,past_minA = maxminA[:,1:2],maxminA[:,2:3]
			past_maxB,past_minB = maxminB[:,1:2],maxminB[:,2:3]

			current_maxA,current_minA = np.array([xA.max(axis=0)]).T,np.array([xA.min(axis=0)]).T
			current_maxB,current_minB = np.array([xB.max(axis=0)]).T,np.array([xB.min(axis=0)]).T
			mmA = np.hstack([past_maxA,current_maxA,past_minA,current_minA]).T
			mmB = np.hstack([past_maxB,current_maxB,past_minB,current_minB]).T
			
			self.maxA,self.minA = np.array([mmA.max(axis=0)]).T,np.array([mmA.min(axis=0)]).T
			self.maxB,self.minB = np.array([mmB.max(axis=0)]).T,np.array([mmB.min(axis=0)]).T	
		
		''' Normalize Input Data '''
		self.xAn,self.xBn = norm(xA,self.maxA,self.minA),norm(xB,self.maxB,self.minB)
		
		''' Complement Code Data '''
		self.IA = np.transpose(np.hstack([self.xAn, 1-self.xAn]))
		self.IB = np.transpose(np.hstack([self.xBn, 1-self.xBn]))
		self.nAB = len(self.IA[0])
		
		if self.update == False:		
			self.TA = np.ones((len(self.IA),1))
			self.TB = np.ones((len(self.IB),1))
			self.L = np.zeros((len(self.IA[0]),len(self.IB[0])))
		else:
			self.ncA_old = len(TA)
			self.ncB_old = len(TB)
			
			self.TA = TA.T	#np.append(TA.T,np.ones((len(TA[0]),8)),1)
			self.TB = TB.T 	#np.append(TB.T,np.ones((len(TB[0]),8)),1)
			self.L = np.append(np.append(L,np.zeros((len(L),8)),1),np.zeros((8,len(np.append(L,np.zeros((len(L),8)),1)[0]))),0)

		self.minA = np.ones((len(xA[0])*2,1))
		self.chAm = np.zeros((len(xA)*10,1))
		self.mA = np.zeros((len(xA)*10,1))
		
		self.minB = np.ones((len(xB[0])*2,1))
		self.chBm = np.zeros((len(xB)*10,1))
		self.mB = np.zeros((len(xB)*10,1))

	def lrBfailed(self,IB,TB,L,cmax,j,ch,nc):
		if self.mB[ch] >= self.rhoB:
			'''
            Update B-Side Category
            Update L  
            '''
			TB = self.UpdateTemplate(IB, TB, cmax, j, ch)
			L[self.ncA-1, ch] = 1 
			
		else:
			'''
            Create new B-Side Category
            Update L
            '''
			self.ncB += 1
			TB = self.CreateTemplate(IB,TB,nc,j)
			L[self.ncA-1, self.ncB-1] = 1
		
		return L, TB
	
	def UpdateTemplate(self,I,T,cmax,j,ch):
		"""
		Update A and B Templates
		
		:param I:		Input
		:param T: 		Template 
		:param cmax:	Maximum choice template
		"""
		p = np.hstack([np.array([I[:,j]]).T,T[:,cmax]])
		T[:,cmax] = np.array([p.min(axis=1)]).T

		return T
		
	def CreateTemplate(self,I,T,nc,j):
		"""
		Create New A and B Templates
		
		:param I:		Input
		:param T: 		Template 
		:param nc:		Number of A or B templates
		"""
		T = np.append(T,np.array([I[:,j]]).T,1)		
		return T

	def lapart_train(self,xA,xB):
		
		"""
		Parameters
		----------
		xA : matrix
		xB " maxtrix
		""" 
		if self.update == False:
			''' Set first template as first input '''
			self.TA[:,0] = self.IA[:,0]
			self.TB[:,0] = self.IB[:,0]
			self.L[0,0] = 1
			self.ncA, self.ncB = 1,1
		else:
			self.ncA, self.ncB = self.ncA_old, self.ncB_old
		
		for ep in range(self.nep):
			for j in range(self.nAB):
			
				cmaxA, chA = ART(self.IA,self.TA,self.mA,self.chAm,self.ncA,self.minA,self.rhoA,self.beta,j)
				
				if cmaxA == -1:
					
					''' 
					++++++++++++ CASE 1 ++++++++++++++++++++++++++++ 
					A-Side => faild vigalance and creates new node
					B-Side => perform as a normal fuzzy ART
					'''
					
					self.ncA += 1
					self.TA = self.CreateTemplate(self.IA,self.TA,self.ncA,j)
					cmaxB, chB = ART(self.IB,self.TB,self.mB,self.chBm,self.ncB,self.minB,self.rhoB,self.beta,j)
					
					if cmaxB == -1:
						self.ncB += 1
						self.TB = self.CreateTemplate(self.IB,self.TB,self.ncB,j)
						self.L[self.ncA-1,self.ncB-1] = 1
					else:
						self.TB = self.UpdateTemplate(self.IB,self.TB,cmaxB,j,chB)
						self.L[self.ncA-1,chB] = 1
					
				else:
					
					''' 
					++++++++++++ CASE 2 ++++++++++++++++++++++++++++ 
					A-Side Resonates
					B-Side must consider primed class B template
					and at the same time reads its input IB
					
					Present B-Side input and Prime B-Side
					Prime = B-Side must consider template associated with A-Side Template
					'''

					cmaxB, chB = ART(self.IB,self.TB,self.mB,self.chBm,self.ncB,self.minB,self.rhoB,self.beta,j)
					
					if cmaxB == -1:
						'''
						B-Side Failed 
						Try Other A and B -Side Templates 
						'''
					
						lr = 1
						lrcount = 1
						while lr == 1:
							self.chAm[chA] = 0
							chA = self.chAm.argmax()
							
							if self.mA[chA] >= self.rhoA:
								'''
								A-Side Passed Vigalance
								'''
								for li in range(self.ncB):
									if self.L[chA,li] == 1:
										chB = li
										if self.mB[chB] >= self.rhoB:
											'''
											B-Side Passed Vigalance
											Update A and B Side
											'''
											cmaxA,cmaxB = chA,chB
											self.TA = self.UpdateTemplate(self.IA,self.TA,cmaxA,j,chA)
											self.TB = self.UpdateTemplate(self.IB,self.TB,cmaxB,j,chB)
											lr = 0
										else:
											if lrcount == self.ncA:
												''' 
												No Match
												Create new A-Side Category
												'''
												self.ncA += 1
												self.TA = self.CreateTemplate(self.IA,self.TA,self.ncA,j)
												#cmaxB, chB = self.ArtB(self.IB,self.TB,j)
												cmaxB, chB = self.ART(self.IB,self.TB,self.mB,self.chBm,self.ncB,self.minB,self.rhoB,j)
												L,TB = self.lrBfailed(self.IB,self.TB,self.L,cmaxB,j,chB,self.ncB)
												lr = 0
											else:
												lr = 0
												lrcount += 1
							else:
								'''
								Next A-Side chA did not pass
								Create new A-Side Template
								'''
								self.ncA += 1
								
								self.TA = self.CreateTemplate(self.IA,self.TA,self.ncA,j)
								cmaxB, chB = ART(self.IB,self.TB,self.mB,self.chBm,self.ncB,self.minB,self.rhoB,self.beta,j)
								#cmaxB,chB = self.ArtB(self.IB,self.TB,j)	
								
								if cmaxB == -1:
									self.ncB += 1
									self.TB = self.CreateTemplate(self.IB,self.TB,self.ncB,j)
									self.L[self.ncA-1,self.ncB-1] = 1
								else:
									self.TB = self.UpdateTemplate(self.IB,self.TB,cmaxB,j,chB)	
									self.L[self.ncA-1,chB] = 1
									
								lr = 0
					else:
						'''
						A and B Side Resonates
						Update A and B Templates
						'''
						self.TA = self.UpdateTemplate(self.IA,self.TA,cmaxA,j,chA)
						self.TB = self.UpdateTemplate(self.IB,self.TB,cmaxB,j,chB)
						
	
			L = self.L[:self.ncA,:self.ncB]
        	TA = np.transpose(self.TA[:,:self.ncA])
        	TB = np.transpose(self.TB[:,:self.ncB])     	
        	
        	return TA,TB,L		
				

def lapArt_train(xA,xB,rhoA=0.9,rhoB=0.9,beta=0.000001,alpha=1.0,nep=1,memory_folder='',update_templates=True):
	
	"""
    
    Parameters
    ----------
    xA : matrix
    xB " maxtrix
    """ 
	
	start_time = time.time()
	
	if update_templates == True:
		TA,TB,L = pd.read_csv('%s/TA.csv'%memory_folder).as_matrix(),pd.read_csv('%s/TB.csv'%memory_folder).as_matrix(),pd.read_csv('%s/L.csv'%memory_folder).as_matrix()
		TA,TB,L = TA[:,1:],TB[:,1:],L[:,1:] 
	else:
		TA,TB,L = [],[],[]	
	
	ann = train(xA,xB,rhoA,rhoB,beta,alpha,nep,TA,TB,L,memory_folder,update_templates)
	TA,TB,L = ann.lapart_train(xA,xB)
	
	TA,TB,L = pd.DataFrame(TA),pd.DataFrame(TB),pd.DataFrame(L)
	TA.to_csv('%s/TA.csv'%memory_folder)
	TB.to_csv('%s/TB.csv'%memory_folder)
	L.to_csv('%s/L.csv'%memory_folder)

	elapsed_time = time.time() - start_time
	
	return TA,TB,L,elapsed_time



if __name__ == '__main__':
    lapArt_train()