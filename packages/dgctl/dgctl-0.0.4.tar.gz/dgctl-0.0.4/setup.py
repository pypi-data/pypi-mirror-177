# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dgctl']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'python-dotenv>=0.0.0']

entry_points = \
{'console_scripts': ['dgctl = dgctl.dgctl:cli']}

setup_kwargs = {
    'name': 'dgctl',
    'version': '0.0.4',
    'description': 'digger.dev client',
    'long_description': 'None',
    'author': 'Mohammed Habib',
    'author_email': 'mo@digger.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
