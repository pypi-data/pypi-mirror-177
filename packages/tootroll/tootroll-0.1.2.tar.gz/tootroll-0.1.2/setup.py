# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tootroll']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'tootroll',
    'version': '0.1.2',
    'description': 'Tootroll is a Python package to read timelines from the Mastodon network.',
    'long_description': '# Tootroll\nTootroll is a Python package to read timelines from the Mastodon network.\n\n## Prerequisites\n### Python\nPython 3.7 or higher is required to run this package.\n\n### Mastodon account (optional)\nTo read public timelines an account is not needed.\n\nA Mastodon account is required to read the Home timeline.\nTo setup a Mastodon account, visit: [joinmastodon.org](https://joinmastodon.org/).\n\nTo acquire a (private) API key ("access token"):\n1. go to "edit profile"\n2. click "<> Development"\n3. click "New application"\nApplication name can be anything. Leave the Redirect URI unchanged. Because we only want to read timelines, we recommend to only check "read" for Scopes. Write and follow is not needed.\n4. click "Submit" and open the link to the created Application\n5. Copy the "access token" (Client key and secret are not needed)\n\n## Install\nThe package can be installed from PyPI:\n```\npython -m pip install tootroll\n```\n\n## Quick setup\n### Configure public (default) profile\nWhen installed for the first time, API keys must be configured.\nTo allow easy switching between servers, public/ private APIs the package allows to define multiple named profiles.\n\nTo setup the default profile, run the following command and follow instructions.\nPick a server from the list or set your own (hostname of Mastodon server).\nFor the default profile, we recommend to say (N)o when asked for private API key.\n```\npython -m tootroll --configure\n```\nTest if it works by getting timeline data for 1 toot.\n```\npython -m tootroll --pub --limit 1\n```\nPipe through a JSON parser\n```\npython -m tootroll --pub --limit 5 |python -m json.tool\n\n```\n\n### Configure private profile\n```\npython -m tootroll --configure --profile myProfile\n```\nWhen asked to use private API, type (Y)es.\nCopy the access token from your Mastodon account.\n\nAll configuration files are stored under ~/.tootroll.\n\n```\npython -m tootroll --home --profile myProfile --limit 5 |python -m json.tool\n```\n\n## Usage\n```\npython -m tootroll --help\n```\n```\nusage: tootroll [-h] [--pub | --home | --tags TAGS | --configure | --show [profiles]] [--profile PROFILE] [-l LIMIT]\n\noptions:\n  -h, --help            show this help message and exit\n  --pub                 Show public timeline of server\n  --home                Show home timeline\n  --tags TAGS           Tag(s). Use comma-separated string to pass a list\n  --configure           Create or update a profile\n  --show [profiles]     Show configuration (e.g. list of profiles)\n  --profile PROFILE     Select a profile to use. If left empty, lists configured profiles\n  -l LIMIT, --limit LIMIT\n                        Limit number of toots. Defaults to 10\n```\n',
    'author': 'Anthony Potappel',
    'author_email': 'anthonyp@lakeclub.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
