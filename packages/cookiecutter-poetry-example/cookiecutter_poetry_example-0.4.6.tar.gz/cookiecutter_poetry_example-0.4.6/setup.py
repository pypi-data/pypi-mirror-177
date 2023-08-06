# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cookiecutter_poetry_example']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cookiecutter-poetry-example',
    'version': '0.4.6',
    'description': 'This is a template repository for Python projects that use Poetry for their dependency management.',
    'long_description': '# cookiecutter-poetry-example\n\n[![Release](https://img.shields.io/github/v/release/fpgmaas/cookiecutter-poetry-example)](https://img.shields.io/github/v/release/fpgmaas/cookiecutter-poetry-example)\n[![Build status](https://img.shields.io/github/workflow/status/fpgmaas/cookiecutter-poetry-example/Main/main)](https://github.com/fpgmaas/cookiecutter-poetry-example/actions/workflows/main.yml?query=branch%3Amain)\n[![codecov](https://codecov.io/gh/fpgmaas/cookiecutter-poetry-example/branch/main/graph/badge.svg)](https://codecov.io/gh/fpgmaas/cookiecutter-poetry-example)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/fpgmaas/cookiecutter-poetry-example)](https://img.shields.io/github/commit-activity/m/fpgmaas/cookiecutter-poetry-example)\n[![License](https://img.shields.io/github/license/fpgmaas/cookiecutter-poetry-example)](https://img.shields.io/github/license/fpgmaas/cookiecutter-poetry-example)\n\nThis is a template repository for Python projects that use Poetry for their dependency management.\n\n- **Github repository**: <https://github.com/fpgmaas/cookiecutter-poetry-example/>\n- **Documentation** <https://fpgmaas.github.io/cookiecutter-poetry-example/>\n\n## Getting started with your project\n\nFirst, create a repository on GitHub with the same name as this project, and then run the following commands:\n\n``` bash\ngit init -b main\ngit add .\ngit commit -m "init commit"\ngit remote add origin git@github.com:fpgmaas/cookiecutter-poetry-example.git\ngit push -u origin main\n```\n\nFinally, install the environment and the pre-commit hooks with \n\n```bash\nmake install\n```\n\nYou are now ready to start development on your project! The CI/CD\npipeline will be triggered when you open a pull request, merge to main,\nor when you create a new release.\n\nTo finalize the set-up for publishing to PyPi or Artifactory, see\n[here](https://fpgmaas.github.io/cookiecutter-poetry-example/features/publishing/#set-up-for-pypi).\nFor activating the automatic documentation with MkDocs, see\n[here](https://fpgmaas.github.io/cookiecutter-poetry-example/features/mkdocs/#enabling-the-documentation-on-github).\nTo enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-poetry-example/features/codecov/).\n\n## Releasing a new version\n\n- Create an API Token on [Pypi](https://pypi.org/).\n- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting \n[this page](https://github.com/fpgmaas/cookiecutter-poetry-example/settings/secrets/actions/new).\n- Create a [new release](https://github.com/fpgmaas/cookiecutter-poetry-example/releases/new) on Github. \nCreate a new tag in the form ``*.*.*``.\n\nFor more details, see [here](https://fpgmaas.github.io/cookiecutter-poetry-example/releasing.html).\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry-example](https://github.com/fpgmaas/cookiecutter-poetry-example).',
    'author': 'Florian Maas',
    'author_email': 'ffpgmaas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fpgmaas/cookiecutter-poetry-example',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<=3.11',
}


setup(**setup_kwargs)
