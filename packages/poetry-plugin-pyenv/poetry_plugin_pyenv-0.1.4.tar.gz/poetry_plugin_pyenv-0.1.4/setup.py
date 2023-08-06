# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_plugin_pyenv']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2,<2.0']

entry_points = \
{'poetry.application.plugin': ['demo = poetry_plugin_pyenv.plugin:PyenvPlugin']}

setup_kwargs = {
    'name': 'poetry-plugin-pyenv',
    'version': '0.1.4',
    'description': '',
    'long_description': "# Poetry Plugin Pyenv\n\nThis package aims to make working with [Poetry](https://python-poetry.org/) and [Pyenv](https://github.com/pyenv/pyenv) a seamless experience.\n\n## Installation\n\nThe easist and *recommended* way to install is using Poetry's `self add` command.\n\n```bash\npoetry self add poetry-plugin-pyenv\n```\n\nIf you used `pipx` to install Poetry you can add the plugin via the `pipx inject` command.\n\n```bash\npipx inject poetry poetry-plugin-pyenv\n```\n\nOtherwise, if you used `pip` to install Poetry you can add the plugin packages via the `pip install` command.\n\n```bash\npip install poetry-plugin-pyenv\n```\n\n## Usage\n\n### Enabling\n\nThis plugin work in conjunction with the [`virtualenvs.prefer-active-python`](https://python-poetry.org/docs/configuration#virtualenvsprefer-active-python-experimental) option. Therefore the first step to using this plugin is enabling that option.\n\nTo enable the option locally you can use the following command.\n\n```bash\npoetry config virtualenvs.prefer-active-python true --local\n```\n\nTo, instead, enable the option globally use the following command.\n\n```bash\npoetry config virtualenvs.prefer-active-python true\n```\n\nOnce enabled this plugin should work transparently to enable seamless interoperability with [Poetry](https://python-poetry.org/) and [Pyenv](https://github.com/pyenv/pyenv). To learn more about what this plugin does behind the scenes see the [Behavior](#behavior) section.\n\n## Behavior\n\n[Poetry Plugin Pyenv](#poetry-plugin-pyenv) works by treating `python` constraint declared in the `tool.poetry.dependencies` of `pyproject.toml` as a source of truth for Pyenv's local python version. To do this it will exercise the following behavior.\n\n### Pyenv already has a local version\n\nIf Pyenv already has a local version it will check if the local version matches the constraint specified in the `pyproject.toml`. If the constraint is not satisfied it will proceed to [selecting a new python version](#selecting-a-new-python-version). If the constraint is satisfied Poetry's virtualenv will be created using the local version thanks to [`virtualenvs.prefer-active-python`](https://python-poetry.org/docs/configuration#virtualenvsprefer-active-python-experimental).\n\n### Pyenv has no local version\n\nIf Pyenv does not have a local version set it will proceed to [selecting a new python version](#selecting-a-new-python-version).\n\n### Selecting a new python version\n\nIf a new python version needs to be selected the list of installable versions available to Pyenv will be checked against the constraint. From this list the latest possible version to satisfy the constraint will be selected. If this version is not installed it will be installed. It will then be set as Pyenv's local version and Poetry's virtualenv will be [re]created.\n",
    'author': 'tjquillan',
    'author_email': 'tjquillan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tjquillan/poetry-plugin-pyenv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
