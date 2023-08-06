# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aepp']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.3.0,<3.0.0',
 'pandas>=1.0.1,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'aepp',
    'version': '0.2.1',
    'description': 'A library that provide easy methods to access the Adobe AEP APIs. Wrapping all endpoints and taking care of token generation for you.',
    'long_description': 'None',
    'author': 'Julien Piccini',
    'author_email': 'piccini.julien@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
