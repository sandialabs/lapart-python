Installation
============

lapart-python requires Python (2.7, 3.4, or 3.5) along with several Python package dependencies. 
Information on installing and using Python can be found at https://www.python.org/. 
Python distributions, such as Anaconda, are recommended to manage the Python interface. 

Pecos can be installed using pip, git, or a downloaded zip file. Note that the pip 
installation will NOT include the examples folder referenced in this manual.

**pip:** To install Pecos using pip::

	pip install pecos 
	
**git**: To install Pecos using git::

	git clone https://github.com/sandialabs/pecos
	cd pecos
	python setup.py install
	
Required Python package dependencies include:

* Pandas [Mcki13]_: used to analyze and store time series data, 
  http://pandas.pydata.org/
* Numpy [VaCV11]_: used to support large, multi-dimensional arrays and matrices, 
  http://www.numpy.org/