# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ciscript']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0', 'pydantic>=1.10.2']

extras_require = \
{':python_version < "3.10"': ['typing-extensions>=4.4.0']}

setup_kwargs = {
    'name': 'ciscript',
    'version': '0.1.1',
    'description': '',
    'long_description': 'None',
    'author': 'Adrian Garcia Badaracco',
    'author_email': 'dev@adriangb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
