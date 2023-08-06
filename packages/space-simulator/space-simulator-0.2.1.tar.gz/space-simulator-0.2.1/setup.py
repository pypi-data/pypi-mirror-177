# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['space_simulator']

package_data = \
{'': ['*']}

install_requires = \
['arcade>=2.6.16,<3.0.0', 'numpy>=1.23.4,<2.0.0', 'scipy>=1.9.3,<2.0.0']

entry_points = \
{'console_scripts': ['space-simulator = space_simulator.game:main']}

setup_kwargs = {
    'name': 'space-simulator',
    'version': '0.2.1',
    'description': '',
    'long_description': '',
    'author': 'Tamles',
    'author_email': 'methacrylon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
