# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anansescanpy']

package_data = \
{'': ['*']}

install_requires = \
['anndata>=0.8.0,<0.9.0',
 'jupyterlab>=3.3.4,<4.0.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.4.4,<2.0.0',
 'scanpy>=1.9.1,<2.0.0',
 'scipy>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'anansescanpy',
    'version': '0.1.7',
    'description': 'implementation of scANANSE for scanpy objects in Python',
    'long_description': '# AnanseScanpy: implementation of scANANSE for Scanpy objects in Python\n[![Anaconda-Server Badge](https://anaconda.org/bioconda/anansescanpy/badges/version.svg)](https://anaconda.org/bioconda/anansescanpy)\n[![PyPI version](https://badge.fury.io/py/anansescanpy.svg)](https://badge.fury.io/py/anansescanpy)\n[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/anansescanpy/README.html)\n[![Anaconda-Server Badge](https://anaconda.org/bioconda/anansescanpy/badges/downloads.svg)](https://anaconda.org/bioconda/anansescanpy)\n\n## Installation\n\nThe most straightforward way to install the most recent version of AnanseScanpy is via conda using PyPI.\n\n### Install package through Conda\nIf you have not used Bioconda before, first set up the necessary channels (in this order!). \nYou only have to do this once.\n```\n$ conda config --add channels defaults\n$ conda config --add channels bioconda\n$ conda config --add channels conda-forge\n```\n\nThen install AnanseScanpy with:\n```\n$ conda install anansescanpy\n```\n\n### Install package through PyPI\n```\n$ pip install anansescanpy\n```\n\n### Install package through GitHub\n```\ngit clone https://github.com/Arts-of-coding/AnanseScanpy.git\ncd AnanseScanpy\nconda env create -f requirements.yaml\nconda activate AnanseScanpy\npip install -e .\n```\n\n## Start using the package\n\n### Run the package either in the console\n```\n$ python3\n```\n\n### Or run the package in jupyter notebook\n```\n$ jupyter notebook\n```\n\n## For extended documentation see our ipynb vignette with PBMC sample data\n### Of which the sample data can be downloaded\n```\n$ wget https://mbdata.science.ru.nl/jsmits/scANANSE/rna_PBMC.h5ad -O scANANSE/rna_PBMC.h5ad\n$ wget https://mbdata.science.ru.nl/jsmits/scANANSE/atac_PBMC.h5ad -O scANANSE/atac_PBMC.h5ad\n```\n',
    'author': 'J Arts (Arts-of-coding)',
    'author_email': 'julian.armando.arts@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Arts-of-coding/AnanseScanpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
