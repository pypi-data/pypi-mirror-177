# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_commits_graph']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'matplotlib>=3.5.2,<4.0.0',
 'pandas>=1.4.2,<2.0.0']

entry_points = \
{'console_scripts': ['git-commits-graph = git_commits_graph.main:main']}

setup_kwargs = {
    'name': 'git-commits-graph',
    'version': '0.1.0',
    'description': 'Display graph of changes in number of lines in project or changed lines',
    'long_description': '# Git commits graph\n\nDisplay plot of changes in repo - count of lines or changed lines\n\n## Installation\n\nUse pip to install the package:\n```sh\n$ pip3 install git-commits-graph\n```\nor pipx to install in isolated environment:\n```sh\n$ pipx install git-commits-graph\n```\n\n## Usage\nplot timeline of both added and removed lines in your repo:\n```sh\n```shell\n$ git-commits-graph your-repo-path -c\n```\n![changes](changes.jpg)\n\nplot lines count evolution in time.\n```shell\n$ git-commits-graph your-repo-path -t\n```\n![lines](lines.jpg)\nto se all options:\n```\n$ git-commits-graph --help\n```\n\n```\nUsage: git-commits-graph [OPTIONS] GIT_DIR\n\nOptions:\n  -b, --branch TEXT               git repository branch to browse.\n  -s, --style TEXT                matplotlib plotting style to use.\n  -c, --changes                   plot timeline of both added and removed\n                                  lines.\n  -t, --total-lines               plot lines count time evolution.\n  -g, --aggregate-by TEXT         aggregate by: Y - year, M - month, W - week,\n                                  D - day\n  -l, --log-scale                 aggregate by day\n  -a, --list-available-plot-styles\n                                  list available plot styles and exit.\n  --help                          Show this message and exit.\n```\n\n\n## Related Projects\n[danielfleischer/git-commits-lines-graph](https://github.com/danielfleischer/git-commits-lines-graph) - A small python script to visualize the number of lines in a project, as a function of time.\n\n## License\n\n[MIT](https://izikeros.mit-license.org/) © [Krystian Safjan](https://safjan.com).\n',
    'author': 'Krystian Safjan',
    'author_email': 'ksafjan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/izikeros/git-commits-graph',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
