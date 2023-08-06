# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myprj']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['myprj = myprj.cli:cli']}

setup_kwargs = {
    'name': 'python-project-poetry-template',
    'version': '0.13.4',
    'description': 'Python Project Poetry Template',
    'long_description': '# Python Project Poetry Template\n\nThis is a template of a python project with all CI/CD tools implemented.\n\n## Features\n\n* `direnv` support\n* `commitizen` support\n* `pre-commit` support\n* Github Actions support\n* Version bumping support\n\nExternal requirements:\n\n* direnv\n* task\n* git-flow\n\n## Understand how it works\n\nMaking new releases with git is not that simple. Actually, this mechanism with the current tools we have does not\nreally support well nomenclature change in the git history. If you want to experiment, you may want to sometime\nreset your git history to start from a fresh clean.\n\n## Howto\n\n### Completely reset the project\n\nLocally:\n\n* # git clone REPO -b <BRANCH_YOU_WANT_TO_KEEP> RESET\n* git clone git@github.com:mrjk/python-project-poetry-template.git -b main RESET\n* cd RESET\n* rm -rf .git\n* git init .\n* git add .\n* git commit -m "Initial commit"\n\nOn github (if you want to clean actions and releases as well):\n\n* Delete your repository\n* Recreate your repo with the same name\n* Ensure in the settings:\n  * Settings/Actions/General\n    * Check: Allow all actions\n  * Settings/Pages\n    * Check: Deploy from branch\n    * Branch: gh_page\n    * Dir: / (root)\n\nFinally, locally:\n\n* git remote add origin git@github.com:<YOUR ACCOUNT>/<YOUR REPOS>.git\n* git push -u --force origin master\n',
    'author': 'mrjk',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://mrjk.github.io/python-project-poetry-template/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
