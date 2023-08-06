# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tsdownsample']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21', 'pandas>=1.3']

setup_kwargs = {
    'name': 'tsdownsample',
    'version': '0.1.0a0',
    'description': 'Time series downsampling in rust',
    'long_description': '# tsdownsample\nTime series downsampling algorithms for visualization\n',
    'author': 'Jeroen Van Der Donckt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/predict-idlab/tsdownsample',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
