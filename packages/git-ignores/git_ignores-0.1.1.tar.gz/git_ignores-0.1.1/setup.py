# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_ignores']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['git-ignores = git_ignores.console:run']}

setup_kwargs = {
    'name': 'git-ignores',
    'version': '0.1.1',
    'description': '.gitignore generator built as a git plugin',
    'long_description': '# git-ignores\n\nGit plugin that generates a .gitignore for your project based on Githubs gitignore templates.\n\n## Usage\n\nThe plugin provides a new git subcommand `ignores`. which takes the following options.\n\n- `--template` - The name of the gitignore template from \n  [this repo](https://github.com/github/gitignore) (_i.e_ `Python` or `Javascript`)\n\n- `--append` - Instead of failing or replacing content, `--append` will tell the \nscript to simply append the gitignore entries instead of replacing the file wholesale.\n\n- `--force` - Replace the .gitignore file by force with the new template.\n\n> You can also run `git-ignores --help` to view the help message. Note that `git ignores --help` returns an error as git tries to load a man page when --help is called. A man-page will be shipped in a future update.\n\n### Example\n\n```\n$ git ignores -t Python --force\n```\n\n## Installation\n\n__FIXME__\n\n## Contributing\n\nIf you wish to contribute to the project. Here a few things to note.\n\n- Python version used in development: 3.11\n- This project uses the [Poetry](https://python-poetry.org/) build tool.\n\n## Todo\n- [ ] Tests\n- [ ] Cleanup and validate package metadata\n- [ ] Publish on PyPi',
    'author': 'Josh Burns',
    'author_email': 'joshyburnss@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
