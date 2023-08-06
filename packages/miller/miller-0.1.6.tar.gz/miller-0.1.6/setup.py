# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miller']

package_data = \
{'': ['*']}

install_requires = \
['camina>=0.1.10,<0.2.0', 'nagata>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'miller',
    'version': '0.1.6',
    'description': 'introspection tools using consistent, accessible syntax',
    'long_description': '[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![PyPI Latest Release](https://img.shields.io/pypi/v/miller.svg)](https://pypi.org/project/miller/) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Documentation Status](https://readthedocs.org/projects/miller/badge/?version=latest)](http://miller.readthedocs.io/?badge=latest)\n\n# What is miller?\n\n*"I\'m a tool that finds things."* - Detective Josephus Miller\n\nNamed after the erstwhile inspector from *The Expanse*, this package provides convenient, simple introspection tools for packages, modules, classes, objects, attributes, and containers. \n\n# Why miller?\n\n## Simple\n\nConsider the different and often difficult-to-read syntax that Python uses for introspection of different objects.\n```\n"""Returns a list of function names in the module \'item\'."""\n[m[0] for m in inspect.getmembers(item, inspect.isfunction)\n if m[1].__module__ == item.__name__]\n"""Returns names of properties of the instance \'item\'."""\n[a for a in dir(item) if isinstance(getattr(a, item), property)] \n"""Returns names of fields of the dataclass \'item\'."""\n[f.name for f in dataclasses.fields(item)] \n```\nThat code can be difficult to remember, requires importing a range of packages, and is not easy to understand if you are not familiar with the relevant imported packages. In contrast, miller uses simple, easy-to-read code for each of the above requests:\n```\nname_functions(item)\nname_properties(item)\nname_fields(item)\n```\nIn addition, each of those **miller** functions includes a boolean parameter `include_privates` which indicates whether you want to include any matching items that have str names beginning with an underscore.\n\n## Intuitive\n\nUnlike the default Python instrospection functions and methods, **miller** uses a consistent syntax and structure that is far more intuitive. This allows users to guess what the appropriate syntax should by following a simple, consistent structure.\n\n**miller** uses four basic prefixes for its core introspection functions:\n \n* `get`: returns the items sought.\n* `has`: returns a bool as to whether a class or object has a list of items.\n* `is`: returns a bool as to whether a class or object is a type.\n* `name`: returns the str names of the items sought.\n  \nThose prefixes are followed by an underscore and a suffix indicating what information is sought. So, for example, \n\n* `get_methods`: returns a dict of the method names and methods of an object.\n* `has_methods`: returns whether an object has all of the named methods passed to the `methods` parameter.\n* `is_method`: returns whether an item is a method of an object.\n* `name_methods`: returns a list of names of methods of an object.\n\n# Contributing \n\nThe project is highly documented so that users and developers can make **miller** work with their projects. It is designed for Python coders at all levels. Beginners should be able to follow the readable code and internal documentation to understand how it works. More advanced users should find complex and tricky problems addressed through efficient code.\n',
    'author': 'Corey Rayburn Yung',
    'author_email': 'coreyrayburnyung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/WithPrecedent/miller',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
