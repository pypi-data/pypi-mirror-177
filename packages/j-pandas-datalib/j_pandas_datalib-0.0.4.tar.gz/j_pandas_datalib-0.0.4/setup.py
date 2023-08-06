# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['j_pandas_datalib']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.0,<1.4.0']

setup_kwargs = {
    'name': 'j-pandas-datalib',
    'version': '0.0.4',
    'description': 'Dataabstractionlayer For Pandas',
    'long_description': '# Python Datalib\n\nUseful Python abstractions around the Pandas file Interaction and other common Tasks.\n\n## VS Code Devcontainer\n\nThis workspace contains a [Vscode devcontainer](https://code.visualstudio.com/docs/remote/containers).\n\n## Gitlab Release\n\nThere are 2 Ways to start a release Pipeline:\n\n1. Via gitlab UI\n   1. Create new Pipeline in CI View\n   2. Supply Variables "`BUMP_VERSION`" [Valid Values](https://python-poetry.org/docs/cli/#version) and optional "`TAG_NOTE`" to add a text to the Git Tag.\n   3. Profit\n2. Via Git while Pushing\n   - Publish a path release: `git push -o ci.variable="BUMP_VERSION=patch"`\n   - Major release with release comment `git push -o ci.variable="BUMP_VERSION=patch" -o ci.variable="TAG_NOTE=This is a super cool new version"`\n',
    'author': 'Joshua Kreuder',
    'author_email': 'joshua_kreuder@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/open-jk-soft/wodoo-datalib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
