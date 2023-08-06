# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_zest']

package_data = \
{'': ['*']}

entry_points = \
{'pytest11': ['zest = pytest_zest']}

setup_kwargs = {
    'name': 'pytest-zest',
    'version': '0.0.1',
    'description': 'Zesty additions to pytest.',
    'long_description': 'None',
    'author': 'Indi Harrington',
    'author_email': 'indigoharrington@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
