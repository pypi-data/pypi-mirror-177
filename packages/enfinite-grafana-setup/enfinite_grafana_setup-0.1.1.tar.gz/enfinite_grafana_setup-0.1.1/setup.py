# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enfinite_grafana_setup']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'enfinite-grafana-setup',
    'version': '0.1.1',
    'description': 'package for managing grafana setup for enfinite clients',
    'long_description': '<div align="center">\n    <p float="left">\n    <img  src="https://enfinite-public.s3.amazonaws.com/enfinite_icon.svg" \n        width="100"\n        height=100>\n    <img  src="https://upload.wikimedia.org/wikipedia/commons/9/9e/Plus_symbol.svg"\n          width="auto"\n          height=100>\n    <img    src="https://grafana.com/static/assets/internal/grafana_logo-web.svg"\n            width="350"\n            height=100>\n    </p>\n</div>\n\n-----------------\n# Enfinite-Grafana-Setup\n[![PyPI Latest Release](https://img.shields.io/badge/pypi-1.0-blue)](https://pypi.org/project/pandas/)\n[![Package Status](https://img.shields.io/badge/status-beta-orange)](https://pypi.org/project/pandas/)\n[![License](https://img.shields.io/badge/license-Enfinite-green)](https://github.com/pandas-dev/pandas/blob/main/LICENSE)\n[![Coverage](https://codecov.io/github/pandas-dev/pandas/coverage.svg?branch=main)](https://codecov.io/gh/pandas-dev/pandas)\n[![Slack](https://img.shields.io/badge/join_Slack-information-brightgreen.svg?logo=slack)](https://pandas.pydata.org/docs/dev/development/community.html?highlight=slack#community-slack)\n# What is this about\nThis appication helps in setup for Grafana, installation, upgrading, whitelabeling and port mapping\n\n# Steps for Upgrading\n## **Test Env:** `EC2:vista-grafana-backup`, `WSL:Ubuntu`\nload env variables in sudo user, either do that manually or add this to your bash.rc in root folder\n```sh\n# .env loading in the shell\ndotenv () {\n  set -a\n  [ -f .env ] && . .env\n  set +a\n}\n\n# Run dotenv on login\ndotenv\n```\nchange the current user to root user\n```sh\n# change the user to root, necessary for editing the grafana files\nsudo -i\n```\npull the repo\n```sh\ngit clone https://github.com/Enfinite-Tech/enfinite-grafana-setup.git\n``` \nchange pwd to the `enfinite-grafana-setup` dir\n```sh\ncd enfinite-grafana-setup\n```\ninstall the grafana package\n```sh\npython3 enfinite-grafana-setup/enfinite_grafana_setup/install_grafana.py\n```\nwhitelabel the grafana installation\n```sh\npython3 enfinite-grafana-setup/app.py\n```\nTest the installation and changes using `pytest`\n```sh\npytest -v\n```\n\n# Environment Variable\n\n| Env Variable  | Description                                                           | \n| ------------- |:---------------------------------------------------------------------:|\n| TITLE         | Title Name to be shown at login screen and in the title of webpages   |\n| APPICON       | Icon link, for setting the icons on title and nav bar                 |\n| FAVICON       | Icon link, for setting the favion on login page                       |\n| LOGIN         | Login page link to get the js files names and locations               |\n\n# Version Release Notes:\n- 0.3\n    - tested and updated app according to ec2 machine: vista-grafana-backup\n    - added steps for upgrading\n- 0.2\n    - upgraded to a newer version and tested [9.2.4]\n    - added a `test/test_login_page.py` to see if it is loading login page\n    - added another command in installation to re-map port 3000->80\n- 0.1 \n    - added all required functions\n    - tested on local wsl, with grafana 9.2\n    - all functions working properly\n\n# Tested Grafana Versions:\n- grafana_9.2.4_amd64.deb\n- grafana_9.2.0_amd64.deb\n\n# To Do\n- Testing the function on backup EC2',
    'author': 'Chirag Gupta (cgupta98)',
    'author_email': 'cgupta@enfinitetech.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Enfinite-Tech/enfinite-grafana-setup/tree/packagev1',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
