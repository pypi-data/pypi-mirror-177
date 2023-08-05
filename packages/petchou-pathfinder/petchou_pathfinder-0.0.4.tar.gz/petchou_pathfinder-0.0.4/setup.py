# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pathfinding']

package_data = \
{'': ['*']}

install_requires = \
['termcolor>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'petchou-pathfinder',
    'version': '0.0.4',
    'description': 'Path finding library for your projects',
    'long_description': '# pathfinding\n\n## Table of content\n- [table of content](#Table-of-content)\n- [Installation](#Installation)\n- [Note](#Note)\n    - [Known issues](#Known-issues-)\n- [Use](#Use)\n    - [Create an instance](#Create-an-instance)\n    - [Steps to find a path](#Steps-to-find-a-path)\n    - [Display the path](#Display-the-path)\n\n## Installation\nYou can install the package by running the following command :\n```python3 -m pip install --upgrade PathFinder``` \n\n## Note \n**Please note** that the package is currently in **beta** version and may encounter **bugs** or **unexpected behaviours** for which **I am not responsible**.\n\n#### Known issues : \n- No cartesian coordinates for grid display available (only alphabetical coordinates)\n- Grid display is not centered and might not work in every terminal\n- The `find_path` method is not optimized and might take a long time to find a path\n\n## Use \n\n### Create an instance \nSimply import the `pathfinding` object from the package into your script and start use it.\n\n```py\nfrom pathfinding import PathFinder as pf\n\n # From Asynconf 2022 - https://asynconf.fr/\nmap = """\nO___O_OO__OO__VO_O_O\n__O___O_OOO_OO_____O\nOO___O___OOO_OOOOO_O\n__OO__X__OO_O___O__O\n_OO___OO______O___OO\n""".split("\\n")\n\npathfinder = pf(\n                        map,         # map to use (list or str)\n                "X",                 # start point (str)\n                "V",                 # end point (str)\n                walkable="_",        # walkable tiles (str)\n                non_walkable="O",    # non walkable tiles (str)\n                debug_mode=False     # display processing informations (bool)\n)\n```\n\n### Steps to find a path\n1. Make a graph from the map\n```py\ngraph = pathfinder.make_graph()\n```\n2. Get the first path found\n```py\npath = pathfinder.find_path()\n```\n3. Optimize the path\n```py\noptimized_path = pathfinder.optimize_path(path)\n```\n4. use the path\n```py\nprint(pathfinder.get_path(alphanumeric=True))\nprint(pathfinder.get_path(alphanumeric=False))\n\n##################################################\n[\'G4\', \'H4\', \'I4\', \'I5\', \'J5\', \'K5\', \'L5\', \'M5\', \'N5\', \'N4\', \'O4\', \'P4\', \'P5\', \'Q5\', \'R5\', \'R4\', \'S4\', \'S3\', \'S2\', \'R2\', \'Q2\', \'P2\', \'O2\', \'O1\']\n[(6, 3), (7, 3), (8, 3), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (13, 3), (14, 3), (15, 3), (15, 4), (16, 4), (17, 4), (17, 3), (18, 3), (18, 2), (18, 1), (17, 1), (16, 1), (15, 1), (14, 1), (14, 0)]\n```\n### Display the path\n```py\nprint(pathfinder.show_path(show_grid=True, animate=False))\n\n##################################################\n# displays the path on the map. If animate is True, the path will be displayed step by step and the screen will be cleared after each step\n```\n\n',
    'author': 'PetchouDev',
    'author_email': 'petchou91d@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/PetchouDev/PathFinder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
