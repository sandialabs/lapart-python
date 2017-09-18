===========================
lapart-python documentation
===========================

The Laterally Primed Adaptive Resonance Theory (LAPART) neural networks couple two Fuzzy ART algorithms to create a mechanism for making 
predictions based on learned associations. The coupling of the two Fuzzy ARTs has a unique 
stability that allows the system to converge rapidly towards a clear solution. Additionally, 
it can perform logical inference and supervised learning similar to fuzzy ARTMAP.

.. _fig-lapart1:
.. figure:: figures/lapart1.png
   :scale: 75 %
   :alt: Sample-graphics
   
   LAPART training (shown on the left side) uses two Fuzzy ART (A&B) algorithms connected by an associator matrix (L).
   During training inputs xi are applied to the A-Side while yi inputs are presented ot the B side.
   The algorithm then produces templates and an L matrix.  The testing processes (shown on the right side) 
   has the same structure as the training but applies previously unseen testing data (xi) to the A-Side.
   The algorithm then produces outputs on the B-Side that are the prediction results.
   


.. toctree::
   :maxdepth: 1
   :caption: Overview:
   
   overview
   installation 
 
.. toctree::
   :maxdepth: 1
   :caption: Examples:
   
   xor  
   
.. toctree::
   :maxdepth: 1
   :caption: Code:
   
   art
   train
   test
   license

		

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Sandia National Laboratories is a multimission laboratory managed and operated by National Technology and 
Engineering Solutions of Sandia, LLC., a wholly owned subsidiary of Honeywell International, Inc., for the 
U.S. Department of Energy's National Nuclear Security Administration under contract DE-NA-0003525.
