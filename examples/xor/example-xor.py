#!/usr/bin/env python

import numpy as np
import pandas as pd
from lapart import train,test

xtrain = pd.read_csv('xor_train.csv').as_matrix()
xAtest = pd.read_csv('xor_test.csv').as_matrix()
xAtrain,xBtrain = xtrain[:,0:2],xtrain[:,2:3]

rA,rB = 0.8,0.8

TA,TB,L,t = train.lapArt_train(xAtrain,xBtrain,rhoA=rA,rhoB=rB,memory_folder='templates',update_templates=False) 
C,T,Tn,df,t = test.lapArt_test(xAtest,rhoA=rA,rhoB=rB,memory_folder='templates') 
print(df)