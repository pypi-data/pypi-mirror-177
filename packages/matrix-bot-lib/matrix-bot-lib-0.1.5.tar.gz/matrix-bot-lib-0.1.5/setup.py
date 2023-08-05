# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matrix_bot_lib']

package_data = \
{'': ['*']}

install_requires = \
['httpx[http2]>=0.23.0,<0.24.0', 'result>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'matrix-bot-lib',
    'version': '0.1.5',
    'description': 'Super early lib for interacting with Matrix',
    'long_description': 'None',
    'author': 'Nicolai Søborg',
    'author_email': 'git@xn--sb-lka.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
