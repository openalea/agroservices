=================================================
Developer Install - Ubuntu (linux)
=================================================

.. contents::

.. warning::
    This installation procedure is not fully tested.

1. Install linux dependencies
-----------------------------
.. code:: shell  

    sudo apt-get update
    sudo apt-get install freeglut3-dev

2. Miniconda installation
-------------------------

Follow official website instruction to install miniconda :

http://conda.pydata.org/miniconda.html

3. Create virtual environment and activate it
---------------------------------------------

.. code:: shell

    conda create --name agroservices python
    source activate agroservices


4. Install dependencies with conda
----------------------------------

.. code:: shell

    conda install -c conda-forge appdirs bs4 pygments colorlog requests requests_cache  

(Optional) Install several packages managing tools :

.. code:: shell
    
    conda install -c conda-forge pytest sphinx sphinx_rtd_theme

5. Install agroservices
-----------------------
.. code:: shell

    git clone https://github.com/H2020-IPM-openalea/agroservices.git
    cd agroservices
    python setup.py install
    cd..

6. Test if installation is well installed (with pytest package)
---------------------------------------------------------------
.. code:: shell

    cd agroservices\test
    pytest 