# agroservices

**authors:** 
* Marc Labadie (marc.labadie@inrae.fr)
* Christian Fournier (christian.fournier@inrae.fr)
* Christophe Pradal (christophe.pradal@inrae.fr)       

**Institutes:** INRAE/CIRAD   
**Licence:**[CeCILL-C](https://cecill.info/licences/Licence_CeCILL-C_V1-en.html)   
**Status:** python package   
**Citation:**(DOI)

## Description

AgroService is a Python package that provides access to IPM Web Services (at least) and a framework to easily implement Web Services wrappers. This package is intended to be close to the webservice. Therefore the requests will have the same API that each web service. The contract of agroservice is to wrap web services API into Python and to convert inputs and outputs. In the end, this package will provide transparent access to IPM Services in Python . It will allow OpenAlea to query and access data services, DSS catologue and thus execution of DSS models.

## Install

### Install conda  
Follow official website instruction to install miniconda : http://conda.pydata.org/miniconda.html

### User

**Create a new environment with agroservice installed in there :**
```
conda create -n agroservices -c conda-forge agroservices
conda activate agroservices
```
**In a existing environment :**
```
conda install -c conda-forge agroservices
```

### From source
```
# Install dependency with conda
conda create -n agroservices -c conda-forge python=3
conda activate agroservices
conda install -c conda-forge appdirs bs4 colorlog requests requests_cache pytest

# Load agroservice and install
git clone https://github.com/H2020-IPM-openalea/agroservices.git
cd agroservices
python setup.py develop

# (Optional) Test your installation
cd test; pytest
```

## Requirements
* python 3.8
* appdirs
* bs4
* colorlog
* requests
* requests_cache

## Documentation
not available for the moment. However each function are documented by docstring
