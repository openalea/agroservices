# agroservices

_________________

[![Docs](https://readthedocs.org/projects/agroservices/badge/?version=latest)](https://agroservices.readthedocs.io/)
[![Build Status](https://github.com/openalea/agroservices/actions/workflows/openalea_ci.yml/badge.svg?branch=master)](https://github.com/openalea/agroservices/actions/workflows/openalea_ci.yml?query=branch%3Amaster)
[![License](https://img.shields.io/badge/License--CeCILL-C-blue)](https://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html)
[![Anaconda-Server Badge](https://anaconda.org/openalea3/agroservices/badges/version.svg)](https://anaconda.org/openalea3/agroservices)

_________________

[Read Latest Documentation](https://agroservices.readthedocs.io/) - [Browse GitHub Code Repository](https://github.com/openalea/agroservices/)

_________________

## Description

"AgroService is a Python package that provides access to IPM Web Services (at least) and a framework to easily implement Web Services wrappers. This package is intended to be close to the webservice. Therefore the requests will have the same API that each web service."

## Install

### Install conda

Follow official website instruction to install miniconda : <http://conda.pydata.org/miniconda.html>

### User

**Create a new environment with agroservices installed in there :**

```bash
mamba create -n agroservices -c conda-forge -c openalea3 openalea.agroservices
mamba activate agroservices
```

**In an existing environment :**

```bash
mamba install -c openalea3 -c conda-forge openalea.agroservices
```

### From source

```bash
# Install dependency with conda
mamba create -n agroservices -f conda/environment.yml
mamba activate agroservices

# Clone agroservice and install
git clone https://github.com/openalea/agroservices.git
cd agroservices
pip install -e .

# (Optional) Test your installation
cd test; pytest
```

## Requirements

* python >= 3.10
* appdirs
* bs4
* colorlog
* requests
* requests_cache
* pygments
* jsf

## Contributing

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

A detailed overview on how to contribute can be found in the [contributing guide](http://virtualplants.github.io/contribute/devel/workflow-github.html#workflow-github).

### Contributors

Thanks to all that ontribute making this package what it is !

<a href="https://github.com/openalea/agroservices/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=openalea/agroservices" />
</a>
