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
 'orgparse>=0.3.1,<0.4.0',
 'selenium>=4.6.0,<5.0.0',
 'webdriver-manager>=3.8.5,<4.0.0']

setup_kwargs = {
    'name': 'html-index-maker',
    'version': '0.1.2',
    'description': 'Scrape local HTML files and generate an index.',
    'long_description': '# HTML Index Maker\n\nScrape local HTML files and generate an index.\n\n## Usage\n\n```shell\npython -m html-index-maker -i ./resources -f .html -o ./data.json\n```\n\nThis will call the module on the resources directory, look for html files and store the result in a given json file.\n\n## Supported Reading Formats\n\n- HTML\n- ORG\n\n## Supported Writing Formats\n\n- JSON\n- JS\n- ORG\n- MARKDOWN\n\n## Changelog\n\n- 0.1.2 Fixed .org missing linebreak\n- 0.1.1 Added support for org, js, md, fixes.\n- 0.1.0 Initial Version',
    'author': 'AlbertoV5',
    'author_email': '58243333+AlbertoV5@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AlbertoV5/html-index-maker',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
