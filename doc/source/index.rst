.. agroservices documentation master file, created by
   sphinx-quickstart on Tue Jun  8 18:49:28 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to agroservices' documentation!
========================================

.. contents::

What is agroservices ?
----------------------
AgroService is a Python package that provides access to IPM Web Services (at least) and a framework to easily implement Web Services wrappers. 
This package is intended to be close to the webservice. 
Therefore the requests will have the same API that each web service. 
The contract of agroservices is to wrap web services API into Python and to convert inputs and outputs.
In the end, this package will provide transparent access to IPM Services in Python . 
It will allow OpenAlea to query and access data services, DSS catalogue and thus execution of DSS models.

Installation
------------
.. toctree::
   ./install/index.rst

Documentation
-------------

Agroservices User Guide
''''''''''''''''''''''''

.. toctree::

   ./user/index.rst


API References
--------------

.. toctree::
   ./references/index.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
