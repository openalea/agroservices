=================================================
Developer Install - Windows
=================================================

.. contents::

1. Miniconda installation
-------------------------

Follow official website instruction to install miniconda :

http://conda.pydata.org/miniconda.html

2. Create virtual environment and activate it
---------------------------------------------

.. code:: shell

    conda create --name agroservices python
    conda activate agroservices


3. Install dependencies with conda
----------------------------------

.. code:: shell

    conda install -c conda-forge appdirs bs4 pygments colorlog requests requests_cache  

(Optional) Install several packages managing tools :

.. code:: shell
    
    conda install -c conda-forge pytest sphinx sphinx_rtd_theme

4. Install agroservices
-----------------------
.. code:: shell

    git clone https://github.com/H2020-IPM-openalea/agroservices.git
    cd agroservices
    python setup.py install
    cd..

5. Test if installation is well installed (with pytest package)
---------------------------------------------------------------
.. code:: shell

    cd agroservices\test
    pytest 

