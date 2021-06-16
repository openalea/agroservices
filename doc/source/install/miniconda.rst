=================================================
Installation with Miniconda (Windows, linux, OSX)
=================================================

0. Install Miniconda
--------------------

Follow official website instruction to install miniconda :

http://conda.pydata.org/miniconda.html

1. Install conda-build if not already installed
-----------------------------------------------

.. code:: shell

    conda install conda-build

2. Create virtual environment and activate it
---------------------------------------------

.. code:: shell

    conda create --name agroservice python
    source activate agroservice

3. Build and install openalea.phenomenal package
------------------------------------------------

.. code:: shell

    cd phenomenal/build_tools/conda
    conda build -c conda-forge -c openalea .
    conda install -c conda-forge -c openalea --use-local agroservice
(Optional) Install several package managing tools :

.. code:: shell

    conda install -c conda-forge notebook pythest sphinx sphinx_rtd_theme 

