# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['preconstruct', 'preconstruct._tests']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'joblib>=1.2.0,<2.0.0',
 'melizalab-gammatone>=0.1.1,<0.2.0',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.1,<2.0.0',
 'parse>=1.19.0,<2.0.0',
 'scipy>=1.7.2,<2.0.0',
 'single-source>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'preconstruct',
    'version': '0.2.3',
    'description': 'creates a dataset that is arranged to facilitate neural decoding',
    'long_description': 'None',
    'author': 'Jonah Weissman',
    'author_email': 'jw5av@virginia.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
