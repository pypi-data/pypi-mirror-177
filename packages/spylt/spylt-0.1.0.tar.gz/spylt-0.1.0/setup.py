# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spylt']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0,<4.0']

setup_kwargs = {
    'name': 'spylt',
    'version': '0.1.0',
    'description': "Back up matplotlib's figure data for easy reproduction",
    'long_description': '# spylt\n\nSimple utility to back up the data necessary to reproduce a matplotlib figure.\n',
    'author': 'Thomas Louf',
    'author_email': 'tlouf+pro@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TLouf/spylt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
