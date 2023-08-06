# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['j_pandas_datalib']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.0,<1.4.0']

setup_kwargs = {
    'name': 'j-pandas-datalib',
    'version': '0.0.5',
    'description': 'Dataabstractionlayer For Pandas',
    'long_description': '# Python Datalib\n\nUseful Python abstractions around the Pandas file Interaction and other common Tasks.\n\n## VS Code Devcontainer\n\nThis workspace contains a [Vscode devcontainer](https://code.visualstudio.com/docs/remote/containers).\n\n## Development\n\n### Bump version\n\n- Run `poetry version <minor|major|patch|...>` [Valid Values for Version target](https://python-poetry.org/docs/cli/#version).\n- Push commit with `[BUMP] Prefix`\n\n### Release\n\n- Create new Release in Github\n- Action will automatically create a Tag and push to pypi\n',
    'author': 'Joshua Kreuder',
    'author_email': 'joshua_kreuder@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/OpenJKSoftware/j-pandas-datalib',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
