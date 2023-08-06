# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['efa_utils']

package_data = \
{'': ['*']}

install_requires = \
['factor-analyzer>=0.4.1,<0.5.0',
 'numpy>=1.23.5,<2.0.0',
 'pandas>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'efa-utils',
    'version': '0.6.2',
    'description': 'Custom utility functions for exploratory factor analysis with the factor_analyzer package.',
    'long_description': '# efa_utils\nCustom utility functions for exploratory factor analysis\n',
    'author': 'Marcel Wiechmann',
    'author_email': 'mail@mwiechmann.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
