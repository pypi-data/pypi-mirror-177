# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pimsclient']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'requests_ntlm>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'pimsclient',
    'version': '0.7.0',
    'description': 'Client for PIMS key_file management swagger web API',
    'long_description': 'None',
    'author': 'sjoerdk',
    'author_email': 'sjoerd.kerkstra@radboudumc.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sjoerdk/pimsclient',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
