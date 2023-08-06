# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sc_use_cases', 'sc_use_cases.siem']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10,<2.0', 'swimlane>=10.9,<11.0']

setup_kwargs = {
    'name': 'sc-use-cases',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Ross Bown',
    'author_email': 'rossbo@softcat.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
