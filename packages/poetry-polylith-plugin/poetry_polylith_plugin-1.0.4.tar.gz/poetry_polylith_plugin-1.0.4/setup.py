# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polylith',
 'polylith.bricks',
 'polylith.development',
 'polylith.diff',
 'polylith.dirs',
 'polylith.files',
 'polylith.info',
 'polylith.interface',
 'polylith.log',
 'polylith.poetry.commands',
 'polylith.poetry_plugin',
 'polylith.project',
 'polylith.readme',
 'polylith.repo',
 'polylith.test',
 'polylith.workspace']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2,<2.0', 'rich>=12.6.0,<13.0.0', 'tomlkit>=0.11.5,<0.12.0']

entry_points = \
{'poetry.application.plugin': ['poetry-polylith-plugin = '
                               'polylith.poetry_plugin:PolylithPlugin']}

setup_kwargs = {
    'name': 'poetry-polylith-plugin',
    'version': '1.0.4',
    'description': 'A Poetry plugin that adds tooling support for the Polylith Architecture',
    'long_description': '# Poetry Polylith Plugin\n\nThis is a Python `Poetry` plugin, adding CLI support for the Polylith Architecture.\n\n\n## What\'s Polylith?\nFrom the [official docs](https://polylith.gitbook.io/polylith/):\n\n>... Polylith is a software architecture that applies functional thinking at the system scale. It helps us build simple, maintainable, testable, and scalable backend systems. ...\n\nPolylith is an architecture (with tooling support) originally built for Clojure.\nWith this Poetry plugin, Polylith is available in Python too!\n\n### An Architecture well suited for Monorepos\nPolylith is using a components-first architecture. Similar to LEGO, components are building blocks.\nA component can be shared across apps, tools, libraries, serverless functions and services.\n\n\n### Differences between the Clojure & Python implementations\nIn the [official docs](https://polylith.gitbook.io/polylith/) for the Clojure implementation,\nthere is a `interface.clj` file that is used to separate an API from the implementation of a component.\n\nThe Python implementation uses the `__init__.py` to accomplish that. In the Python implementation, the `pyproject.toml` is used to define bases and components.\nIn particular, the `packages` property is used for that.\n\nThis is an example of the _top level_ `pyproject.toml` used when _developing_. This is where you add all bricks (components and bases).\n\n``` shell\n packages = [\n    {include = "development"},\n    {include = "my_namespace/my_component", from = "components"},\n    {include = "my_namespace/my_example_aws_lambda", from = "bases"},\n]\n```\n(using the `loose` theme, see more about that below)\n\nWhen creating a project, the _project specific_ `pyproject.toml` will include all the used components and bases.\nNote that the packages are referenced relative to the project. This is made possible by the Multiproject Poetry plugin.\n\nThis is where you add the bricks used by the actual project.\n\n``` shell\n packages = [\n    {include = "my_namespace/my_component", from = "../../components"},\n    {include = "my_namespace/my_example_aws_lambda", from = "../../bases"},\n]\n```\n\n## Usage\n\n### Install Poetry & plugins\nWith the `Poetry` version 1.2 or later installed, you can add plugins.\n\nAdd the [Multiproject](https://github.com/DavidVujic/poetry-multiproject-plugin) plugin, that will enable the very important __workspace__ support to Poetry.\n``` shell\npoetry self add poetry-multiproject-plugin\n```\n\nAdd the Polylith plugin:\n``` shell\npoetry self add poetry-polylith-plugin\n```\n\n### Create a repository\nCreate a directory for your code, initialize it with __git__ and create a basic __Poetry__ setup:\n\n``` shell\ngit init\n\npoetry init\n```\n\n### Commands\nThe `create workspace` command will create a Polylith workspace, with a basic Polylith folder structure.\n\n\n#### Create\n``` shell\npoetry poly create workspace --name my_namespace --theme <tdd or loose>\n```\n\n*New:* `theme` is a new Python Polylith feature and defines what kind of component structure - or theme - to use.\n\n`tdd` is the default and will set the structure according to the original Polylith Clojure implementation, such as:\n`components/<package>/src/<namespace>/<package>` with a corresponding `test` folder.\n\n`loose` is a new theme, for a more familiar structure for Python:\n`components/<namespace>/<package>` and will put a `test` folder at the root of the repository.\n\n\nAdd a component:\n\n``` shell\n# This command will create a component - i.e. a Python package in a namespaced folder.\npoetry poly create component --name my_component\n```\n\nAdd a base:\n\n``` shell\n# This command will create a base - i.e. a Python package in a namespaced folder.\npoetry poly create base --name my_example_aws_lambda\n```\n\nAdd a project:\n\n``` shell\n# This command will create a project - i.e. a pyproject.toml in a project folder. No code in this folder.\npoetry poly create project --name my_example_aws_lambada_project\n```\n\n#### Info\nShow info about the workspace:\n\n``` shell\npoetry poly info\n```\n\nShows what has changed since the most recent stable point in time:\n\n``` shell\npoetry poly diff\n```\n\nThe `diff` command will compare the current state of the repository, compared to a `git tag`.\nThe tool will look for the latest tag according to a certain pattern, such as `stable-*`.\nThe pattern can be configured in `workspace.toml`.\n\nThe `diff` command is useful in a CI environment, to determine if a project should be deployed or not.\nThe command has a `--short` flag to only print a comma separated list of changed projects to the standard output.\n\n\nUseful for CI:\n``` shell\npoetry poly diff --short\n```\n\n#### Testing\nThe `create` commands will also create corresponding unit tests. It is possible to disable thi behaviour\nby setting `enabled = false` in the `workspace.toml` file.\n\n\n#### Workspace configuration\nAn example of a workspace configuration:\n\n``` shell\n[tool.polylith]\nnamespace = "my_namespace"\ngit_tag_pattern = "stable-*"\n\n[tool.polylith.structure]\ntheme = "loose"\n\n[tool.polylith.test]\nenabled = true\n```\n',
    'author': 'David Vujic',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/davidvujic/python-polylith',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
