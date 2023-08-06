# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quicklook']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0', 'numpy>=1.23.4,<2.0.0']

setup_kwargs = {
    'name': 'quicklook',
    'version': '0.1.1',
    'description': 'An easy way to view numpy arrays',
    'long_description': '# quicklook\nAn easy way to view numpy arrays\n',
    'author': 'Sam Murphy',
    'author_email': 'samsammurphy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
