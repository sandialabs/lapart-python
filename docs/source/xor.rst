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

    rA,rB = 0.8,0.8

.. code:: python

    TA,TB,L,t = train.lapArt_train(xAtrain,xBtrain,rhoA=rA,rhoB=rB,memory_folder='templates',update_templates=False)

.. code:: python

    TA




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.8</td>
          <td>0.8</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>2</th>
          <td>0.0</td>
          <td>0.8</td>
          <td>0.9</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>3</th>
          <td>0.9</td>
          <td>0.9</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    TB




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>0</th>
          <th>1</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>0.0</td>
          <td>0.9</td>
        </tr>
        <tr>
          <th>1</th>
          <td>0.8</td>
          <td>0.0</td>
        </tr>
      </tbody>
    </table>
    </div>


