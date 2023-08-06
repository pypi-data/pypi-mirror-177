# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sendgrid_cli']

package_data = \
{'': ['*']}

install_requires = \
['sendgrid>=6.9.7,<7.0.0']

entry_points = \
{'console_scripts': ['sendgrid = sendgrid_cli.cli:main']}

setup_kwargs = {
    'name': 'sendgrid-cli',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Teddy Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tddschn/sendgrid-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
