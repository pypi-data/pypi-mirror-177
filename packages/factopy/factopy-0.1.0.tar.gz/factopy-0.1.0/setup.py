# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['factopy']

package_data = \
{'': ['*']}

install_requires = \
['jax>=0.3.24,<0.4.0',
 'jaxlib>=0.3.24,<0.4.0',
 'pandas>=1.5.1,<2.0.0',
 'scikit-learn>=1.1.3,<2.0.0']

setup_kwargs = {
    'name': 'factopy',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Factopy\n[![codecov](https://codecov.io/gh/serinir/factopy/branch/main/graph/badge.svg?token=VWQAZUVBN1)](https://codecov.io/gh/serinir/factopy)\n\nA Matrix Factorisation and Dimensionality reduction module \n',
    'author': 'serinirio',
    'author_email': 'imadom568@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/serinir/factopy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
