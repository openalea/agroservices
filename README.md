[![Documentation Status](https://readthedocs.org/projects/agroservices/badge/?version=latest)](https://agroservices.readthedocs.io/en/latest/?badge=latest)
[![Anaconda-Server Badge](https://anaconda.org/openalea3/agroservices/badges/downloads.svg)](https://anaconda.org/openalea3/agroservices)
[![Anaconda-Server Badge](https://anaconda.org/openalea3/agroservices/badges/version.svg)](https://anaconda.org/openalea3/agroservices)
[![Anaconda-Server Badge](https://anaconda.org/openalea3/agroservices/badges/license.svg)](https://anaconda.org/openalea3/agroservices)
# agroservices

**authors:** 
* [Marc Labadie](https://github.com/mlabadie)
* [Christian Fournier](https://github.com/christian34)
* [Christophe Pradal](https://github.com/pradal)       

**Institutes:** INRAE/CIRAD   
**Licence:**[GPL-3](https://www.gnu.org/licenses/gpl-3.0.txt)  
**Status:** python package   
**Citation:**(DOI)

## Description

AgroService is a Python package that provides access to IPM Web Services (at least) and a framework to easily implement Web Services wrappers. This package is intended to be close to the webservice. Therefore the requests will have the same API that each web service. The contract of agroservice is to wrap web services API into Python and to convert inputs and outputs. In the end, this package will provide transparent access to IPM Services in Python . It will allow OpenAlea to query and access data services, DSS catologue and thus execution of DSS models.

## Install


### Install pip  
Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate
```
Install the package:
```bash
pip install . # -e for editable mode
```

### Install conda  
Follow official website instruction to install miniconda : http://conda.pydata.org/miniconda.html

### User

**Create a new environment with agroservices installed in there :**
```
conda create -n agroservices -c conda-forge -c openalea3 agroservices
conda activate agroservices
```
**In an existing environment :**
```
conda install -c openalea3 -c conda-forge agroservices
```

### From source
```
# Install dependency with conda
conda create -n agroservices -c conda-forge python appdirs bs4 pygments colorlog requests requests_cache pytest jsf
conda activate agroservices

# Clone agroservice and install
git clone https://github.com/openalea/agroservices.git
cd agroservices
pip install -e .

# (Optional) Test your installation
cd test; pytest
```

## Requirements
* python >= 3.6
* appdirs
* bs4
* colorlog
* requests
* requests_cache
* pygments
* jsf

## Documentation

You can see the complete documentation with tutorials at: xxx

## Contributing
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

A detailed overview on how to contribute can be found in the [contributing guide](http://virtualplants.github.io/contribute/devel/workflow-github.html#workflow-github).

### contributors

<a href="https://github.com/openalea/agroservices/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=H2020-IPM-openalea/agroservices" />
</a>

