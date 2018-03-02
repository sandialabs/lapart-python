=================
Example: Solar PV
=================

.. code:: python

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

.. code:: python

    from lapart import train,test

.. code:: python

    df = pd.read_csv('pv_train.csv')
    df = df.set_index('datetime')
    df.index = pd.to_datetime(df.index)
    df = df[df['POAIrrad1_Avg'] > 0] 

.. code:: python

    strain,etrain = '2017-03-01 00:00:00','2017-03-28 23:59:00'
    stest,etest = '2017-03-29 07:00:00','2017-03-31 18:59:00'
    dftrain = df[(df.index >= strain) & (df.index <= etrain)]
    dftest = df[(df.index >= stest) & (df.index <= etest)]

.. code:: python

    dftrain = df.sample(frac=0.5)

.. code:: python

    xAtrain = np.array([dftrain['POAIrrad1_Avg'].tolist()]).T  # Plane of Array Irradiance
    xBtrain = np.array([dftrain['Sys1Wdc_Avg'].tolist()]).T    # System 1 DC Power
    xAtest = np.array([dftest['POAIrrad1_Avg'].tolist()]).T    # Plane of Array Irradiance

.. code:: python

    rA,rB = 0.97,0.98

.. code:: python

    TA,TB,L,time_train = train.lapArt_train(xAtrain,xBtrain,rhoA=rA,rhoB=rB,memory_folder='templates',update_templates=False) 

.. code:: python

    C,T,Tn,df,time_test = test.lapArt_test(xAtest,rhoA=rA,rhoB=rB,memory_folder='templates')

.. code:: python

    dfn = pd.DataFrame(Tn,columns=['low', 'high'])

.. code:: python

    dftest['low'] = Tn[:,0].tolist()
    dftest['high'] = Tn[:,1].tolist()

.. code:: python

    #fig = plt.figure(figsize=(20, 10))
    fig, (ax1) = plt.subplots(1,1,figsize=(20, 10))
    ax1.plot(dftest['low'],color='grey')
    ax1.plot(dftest['high'],color='grey')
    ax1.fill_between(dftest.index, dftest['low'], dftest['high'], alpha=0.5,color='grey')
    ax1.plot(dftest.index,dftest['Sys1Wdc_Avg'],color='red')
    ax1.set_xlabel('Time',fontsize=20)
    ax1.set_ylabel('Power (Watts)',fontsize=20)
    ax1.tick_params(axis = 'both', which = 'major', labelsize = 18)
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.grid()
    
    plt.show()



.. image:: output_11_0.png


.. code:: python

    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(20, 10),sharey=True)
    ax1.scatter(dftest['POAIrrad1_Avg'],dftest['Sys1Wdc_Avg'])
    ax1.set_xlabel('Irradiance (W/m$^2$)',fontsize=15)
    ax1.set_ylabel('Power (Watts)',fontsize=15)
    ax1.tick_params(axis = 'both', which = 'major', labelsize = 18)
    ax1.grid()
    
    ax2.scatter(dftest['Sys1Wdc_Avg'],dftest['high'],color='r')
    ax2.scatter(dftest['Sys1Wdc_Avg'],dftest['low'],color='b')
    ax2.set_xlabel('Actual Power (Watts)',fontsize=18)
    ax2.set_ylabel('Estimated Power (Watts)',fontsize=18)
    ax2.tick_params(axis = 'both', which = 'major', labelsize = 18)
    ax2.grid()
    
    
    plt.show()



.. image:: output_12_0.png

