# agroservice

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

* **Install conda**  
Follow official website instruction to install miniconda : http://conda.pydata.org/miniconda.html

#### User

**Create a new environment with agroservice installed in there :**
```
conda create -n agroservice -c conda-forge agroservice
conda activate agroservice
```
**In a existing environment :**
```
conda install -c conda-forge agroservice
```

#### From source
```
# Install dependency with conda
conda create -n agroservice -c conda-forge python=3
conda activate agroservice
conda install -c conda-forge -c bioservice pytest

# Load agroservice and install
git clone https://github.com/H2020-IPM-openalea/agroservice.git
cd agroservice
python setup.py develop

# (Optional) Test your installation
cd test; pytest
```

## Requierments
* python 3.8
* bioservice

## Documentation
not available for the moment. However each function are documented by docstring
