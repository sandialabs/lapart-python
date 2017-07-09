============
Example: XOR
============

The exclusive or (XOR) is a logical operation that outputs true when inputs differ.


.. code:: python

    import numpy as np
    import pandas as pd

.. code:: python

    from lapart import train,test

.. code:: python

    xtrain = pd.read_csv('xor_train.csv').as_matrix()

.. code:: python

    xAtest = pd.read_csv('xor_test.csv').as_matrix()

.. code:: python

    xAtrain,xBtrain = xtrain[:,0:2],xtrain[:,2:3]

.. code:: python

    xAtrain

.. parsed-literal::

    array([[ 0. ,  0. ],
           [ 1. ,  0. ],
           [ 0. ,  1. ],
           [ 1. ,  1. ],
           [ 1. ,  1. ],
           [ 0.9,  0.9],
           [ 0.1,  0.8],
           [ 0.2,  0.2],
           [ 1. ,  1. ]])



.. code:: python

    xBtrain

.. parsed-literal::

    array([[ 0. ],
           [ 1. ],
           [ 1. ],
           [ 0. ],
           [ 0. ],
           [ 0.1],
           [ 0.8],
           [ 0. ],
           [ 0. ]])

.. code:: python

    xAtest

.. parsed-literal::

    array([[ 0.1 ,  0.9 ],
           [ 1.  ,  0.  ],
           [ 0.  ,  0.  ],
           [ 1.  ,  1.  ],
           [ 0.  ,  1.  ],
           [ 0.15,  0.1 ]])

.. code:: python

    rA,rB = 0.8,0.8

.. code:: python

    TA,TB,L,t = train.lapArt_train(xAtrain,xBtrain,rhoA=rA,rhoB=rB,memory_folder='templates',update_templates=False)

.. code:: python

    C,T,Tn,df,t = test.lapArt_test(xAtest,rhoA=rA,rhoB=rB,memory_folder='templates') 

.. code:: python

    C

.. parsed-literal::

    array([[ 1.],
           [ 1.],
           [ 0.],
           [ 0.],
           [ 1.],
           [ 0.]])

