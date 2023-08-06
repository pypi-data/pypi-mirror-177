# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multisearch', 'multisearch.interface']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['ms = multisearch.interface.tui:main']}

setup_kwargs = {
    'name': 'multi-search',
    'version': '0.2.0',
    'description': 'organize and call multiple scripts at once via a plugin style pattern',
    'long_description': 'None',
    'author': 'tyler jones',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
