# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splatlog', 'splatlog.json', 'splatlog.lib', 'splatlog.verbosity']

package_data = \
{'': ['*']}

install_requires = \
['rich>=9', 'typeguard>=2.13.3,<3.0.0']

setup_kwargs = {
    'name': 'splatlog',
    'version': '0.3.0',
    'description': "Python logger that accepts ** values and prints 'em out.",
    'long_description': "splatlog\n==============================================================================\n\nPython logger that accepts ** values and prints 'em out.\n",
    'author': 'nrser',
    'author_email': 'neil@neilsouza.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
