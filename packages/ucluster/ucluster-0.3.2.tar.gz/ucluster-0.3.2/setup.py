# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ucluster', 'ucluster.vd']

package_data = \
{'': ['*']}

install_requires = \
['fasttext>=0.9.2,<0.10.0',
 'hdbscan>=0.8.29,<0.9.0',
 'loguru>=0.6.0,<0.7.0',
 'nltk>=3.7,<4.0',
 'visidata>=2.10,<3.0']

setup_kwargs = {
    'name': 'ucluster',
    'version': '0.3.2',
    'description': 'Text-based clustering utility',
    'long_description': None,
    'author': 'R. Miles McCain',
    'author_email': 'github@sendmiles.email',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
