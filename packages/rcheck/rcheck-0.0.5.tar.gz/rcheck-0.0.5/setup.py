# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rcheck', 'rcheck.checks']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rcheck',
    'version': '0.0.5',
    'description': 'Runtime type checking',
    'long_description': '# `rcheck`\n\nRuntime type checking.\n\n---\n\nFunctions that return a boolean:\n* `is_<type>` such as `is_int`, `is_bool`, etc...\n* `is_opt_<type>` such as `is_opt_int`, `is_opt_bool`, etc.. for optional types\n\nFunctions that raise exceptions:\n* `assert_<type>` such as `assert_int`, `assert_bool`, etc...\n* `assert_opt_<type>` such as `assert_opt_int`, `assert_opt_bool`, etc... for optional types\n',
    'author': 'Alex Rudolph',
    'author_email': 'alex3rudolph@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.github.com/alrudolph/rcheck',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
