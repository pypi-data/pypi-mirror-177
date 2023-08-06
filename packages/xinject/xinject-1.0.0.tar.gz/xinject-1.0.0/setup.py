# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xinject', 'xinject._private']

package_data = \
{'': ['*']}

install_requires = \
['xsentinels>=1.2.0,<2.0.0']

entry_points = \
{'pytest11': ['xinject_pytest_plugin = xinject.pytest_plugin']}

setup_kwargs = {
    'name': 'xinject',
    'version': '1.0.0',
    'description': 'Lazy dependency injection.',
    'long_description': 'None',
    'author': 'Josh Orr',
    'author_email': 'josh@orr.blue',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
