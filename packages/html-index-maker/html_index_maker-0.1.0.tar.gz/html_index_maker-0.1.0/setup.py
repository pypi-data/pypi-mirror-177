# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['html-index-maker']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'selenium>=4.6.0,<5.0.0',
 'webdriver-manager>=3.8.5,<4.0.0']

setup_kwargs = {
    'name': 'html-index-maker',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'AlbertoV5',
    'author_email': '58243333+AlbertoV5@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
