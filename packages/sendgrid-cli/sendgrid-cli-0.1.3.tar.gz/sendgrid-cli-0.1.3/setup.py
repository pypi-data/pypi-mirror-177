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
    'version': '0.1.3',
    'description': '',
    'long_description': "# sendgrid-cli\n\nA very simple SendGrid CLI written in Python with only basic functionalities (at this moment).\n\nThe official [sendgrid-cli](https://github.com/sendgrid/sendgrid-cli) hasn't been updated in years and I couldn't get it to work,  \nso I wrote this with only the features I need.\n\nIf you need more features, feel free to contribute by submitting pull requests.\n\n- [sendgrid-cli](#sendgrid-cli)\n  - [Installation](#installation)\n    - [pipx](#pipx)\n    - [pip](#pip)\n  - [Usage](#usage)\n    - [On the command line](#on-the-command-line)\n    - [On GitHub Actions](#on-github-actions)\n  - [Develop](#develop)\n\n\n## Installation\n\n### pipx\n\nThis is the recommended installation method.\n\n```\n$ pipx install sendgrid-cli\n```\n\n### [pip](https://pypi.org/project/sendgrid-cli/)\n\n```\n$ pip install sendgrid-cli\n```\n\n## Usage\n\n### On the command line\n\n```\nusage: sendgrid [-h] [-V] [-t str [str ...]] [-f str] [-n str] [-s str]\n\nsendgrid CLI\n\noptions:\n  -h, --help            show this help message and exit\n  -V, --version         show program's version number and exit\n  -t str [str ...], --to-emails str [str ...]\n                        To emails (default: None)\n  -f str, --from-email str\n                        From email EMAIL (default: None)\n  -n str, --from-name str\n                        From name NAME (default: None)\n  -s str, --subject str\n                        Subject (default: None)\n\nEmail body (HTML) is read from stdin, supply your API key with SENDGRID_API_KEY environment variable\n\n```\n\n### On GitHub Actions\n\nBelow is a working job configuration\n\n```yaml\n  send-mail:\n    runs-on: ubuntu-latest\n    steps:\n      - name: setup python 3.10\n        uses: actions/setup-python@v4\n        with:\n          python-version: '3.10'\n      - name: install CLI tools\n        run: pipx install sendgrid-cli\n      - name: Send email\n        env:\n          SENDGRID_API_KEY: ${{ secrets.SENDGRID_API_KEY }}\n        run: |\n          cat email-body.html | sendgrid -f 'from@example.com' -n 'from-name' -t 'to@example.com' -s 'sendgrid-cli test'\n```\n\n## Develop\n\n```\n$ git clone https://github.com/tddschn/sendgrid-cli.git\n$ cd \n$ poetry install\n```",
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
