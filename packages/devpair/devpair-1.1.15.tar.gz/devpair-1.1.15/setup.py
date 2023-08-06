# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['app']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.29,<4.0.0',
 'click>=8.0.4,<9.0.0',
 'cowsay>=5.0,<6.0',
 'loguru>=0.6.0,<0.7.0',
 'python-dateutil>=2.8.2,<3.0.0']

entry_points = \
{'console_scripts': ['devpair = devpair:exec_cli']}

setup_kwargs = {
    'name': 'devpair',
    'version': '1.1.15',
    'description': 'Pair script that manage a pair programming session using git.',
    'long_description': '<div align="center">\n    <img src="https://illustrations.popsy.co/amber/communication.svg" width="200px">\n</div>\n\n## Dev Pair\n\n<small>Illustration by: [popsy](https://popsy.co/)</small>\n\n[![Python Test](https://github.com/raphaelkieling/pair/actions/workflows/push.yml/badge.svg)](https://github.com/raphaelkieling/pair/actions/workflows/push.yml)\n![PyPI Version](https://img.shields.io/pypi/v/devpair)\n![Python Version](https://img.shields.io/pypi/pyversions/devpair)\n\nIt\'s a tool to facilitate the remote pair programming session. Instead of make a lot of `git add, git commit, git push, git pull`, you can make it more quickly only running `devpair start <timer optional>` to start coding and `devpair next` to send the code to another person.\n\nVery useful for teams that like to make pair sessions often. If you never was a driver or a navigator feel free to read [here](https://martinfowler.com/articles/on-pair-programming.html) to have a context.\n\n## Install\n\n```\npip install devpair\n```\n\n## Commands\n\n- `devpair start <time in minutes optional>` Start a new session inside the current branch.\n- `devpair next` Save everything and send to the next person.\n- `devpair done` Finish and put all the work in the original branch.\n- `devpair summary` Show a simple resume of commit counts and last developer.\n- `devpair cow` It\'s cow.\n- `devpair timer <time in minutes>` Create a simple timer for any purposal.\n- `devpair --help` I like to have a help some times.\n\n> We recommend to create some alias if you want, like: `dvs` to run `devpair start`, `dvn` to run `devpair next` and `dvd` to run `devpair done`.\n\n## Example of use\n\n```bash\n# Dev A\nmain $ devpair start 10 # Will start the new branch with a 10 minutes timer\npair/main $ echo "hello" > welcome.txt\npair/main $ devpair next\n\n# Dev B\nmain $ devpair start\npair/main $ cat welcome.txt # shows "hello"\npair/main $ echo " world" >> welcome.txt\npair/main $ devpair next\n\n# Dev A\npair/main $ devpair start\npair/main $ cat welcome.txt # shows "hello world"\npair/main $ echo "!" >> welcome.txt\npair/main $ devpair done\n\nmain $ git commit -m "feat: created hello world feature"\nmain $ git push\n\n# Dev B\npair/main $ devpair done # just to come back to the original branch\nmain\n```\n\n## How it works internally?\n\nYou will work inside a temporary pair branch that in the end all the commits will be squashed to be added to the feature branch.\n\n<details>\n    <summary>More details!</summary>\n\nOk ok! Under the hood the `devpair start` will take your current branch and create a copy with the same name but with the prefix `pair`\n\nAfter make your code changes the `devpair next` will add, commit and push your code using an internal commit message. This step will be more easier to understand checking the [example step by step](#example-of-use)\n\nIn the end, we have the `devpair done` that will add, commit, push and delete the branch. Don\'t worry we will make a squash commit of everything that you did for the current branch.\n\n[![](https://mermaid.ink/img/pako:eNqNkMEKwjAMhl9l5Dzx3rPgA3jtJbb_1uLajpgiMvbu1oOgDGE5fSTfn0AWcsWDDI1Rz8JzsLlr5UpKUbd8Fc4udBmPwwDWKtjlzxzluDv0wwHuVqpuTybIiH-bP6nEMX_rG5N6apOm-faD5d2zpAEJlkxDj4HrpJZsXpvKVcvlmR0ZlYqe6uxZcYo8CicyA093rC_K-3GZ?type=png)](https://mermaid.live/edit#pako:eNqNkMEKwjAMhl9l5Dzx3rPgA3jtJbb_1uLajpgiMvbu1oOgDGE5fSTfn0AWcsWDDI1Rz8JzsLlr5UpKUbd8Fc4udBmPwwDWKtjlzxzluDv0wwHuVqpuTybIiH-bP6nEMX_rG5N6apOm-faD5d2zpAEJlkxDj4HrpJZsXpvKVcvlmR0ZlYqe6uxZcYo8CicyA093rC_K-3GZ)\n\n</details>\n\n## Recommendations\n\n- Before the pair programming\n  - Define the end of the session. How many time do you want pair?\n  - Define the break time.\n- Use a `timer`, maybe `devpair` timer or any other one, the important thing is to keep the pair rotation:\n  - `devpair start <time in minutes>`\n  - https://cuckoo.team/\n  - https://double-trouble.wielo.co/\n  - http://mobtimer.zoeetrope.com/\n  - ANY other mobile app, web tool, smartwatch app, pomodoro timer and so on.\n- The `driver` need to share the screen avoiding to use tools like `vscode live share`, even they are good it can create some hard moments that you want to show the browser or create a quickly diagram. The preference is that the `driver` ever need to share the screen.\n- Antipatterns: https://tuple.app/pair-programming-guide/antipatterns\n\n## Contributing\n\nFork, create a branch from `main` with the pattern `feat/my-feature` and make a pull request with your proposal.\n\n## Local env\n\nWe are using [poetry](https://python-poetry.org/) and [pyenv](https://github.com/pyenv/pyenv) to manage all the python versions and dependencies.\n\n```sh\n# Install all the dependencies\npoetry install\n# Install the pre-commit\npoetry run pre-commit install\n# Set the version of the `.python-version`\npyenv local\n# Run all the tests\nmake unit\n```\n\n## Publishing\n\n```sh\nsh ./scripts/tag-new-version.bash v0.0.0\n```\n',
    'author': 'raphael.kieling',
    'author_email': 'raphael.kieling@telus.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
