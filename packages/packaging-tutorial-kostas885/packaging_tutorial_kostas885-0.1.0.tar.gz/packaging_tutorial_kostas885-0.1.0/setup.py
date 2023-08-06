# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['packaging_tutorial']

package_data = \
{'': ['*']}

install_requires = \
['flask>=2.2.2,<3.0.0']

setup_kwargs = {
    'name': 'packaging-tutorial-kostas885',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'developers',
    'author_email': 'kostas@alumnireach.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
