# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['upgrade_knausj',
 'upgrade_knausj.conditions',
 'upgrade_knausj.stdio',
 'upgrade_knausj.steps',
 'upgrade_knausj.types']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3.1.29,<4.0.0',
 'pyyaml>=6.0,<7.0',
 'rich>=12.6.0,<13.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['upgrade-knausj = upgrade_knausj.main:app']}

setup_kwargs = {
    'name': 'upgrade-knausj',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Upgrade `knausj`\n\nHelper for performing `knausj` upgrades.\n\n## Assumptions\n\n- You have a fork of `knausj`\n\n## Installation\n\n1. Install [`pipx`](https://pypa.github.io/pipx/)\n2. `pipx install knausj-upgrade`\n\n## How to run\n\n1. Push your changes to your fork\n2. Run `knausj-upgrade`\n3. Perform any necessary merges, then re-run `knausj-upgrade`\n4. Repeat steps 3-4 until it says you're done\n",
    'author': 'Pokey Rule',
    'author_email': '755842+pokey@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
