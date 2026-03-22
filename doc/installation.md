# Installation

You must use conda environment : <https://docs.conda.io/en/latest/index.html>

## Users

### Create a new environment with agroservices installed in there

```bash

mamba create -n agroservices -c openalea3 -c conda-forge  openalea.agroservices
mamba activate agroservices
```

Install agroservices in a existing environment

```bash
mamba install -c openalea3 -c conda-forge openalea.agroservices
```

### (Optional) Test your installation

```bash
mamba install -c conda-forge pytest
git clone https://github.com/openalea/agroservices.git
cd agroservices/test; pytest
```

## Developers

### Install From source

```bash
# Install dependency with conda
mamba env create -n agroservices -f conda/environment.yml
mamba activate agroservices

# Clone agroservices and install
git clone https://github.com/openalea/agroservices.git
cd agroservices
pip install .

# (Optional) Test your installation
cd test; pytest
```
