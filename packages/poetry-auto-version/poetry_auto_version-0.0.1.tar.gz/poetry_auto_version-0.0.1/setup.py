# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_auto_version']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.2,<2.0.0']

extras_require = \
{'testing': ['pytest>=7.0,<8.0']}

entry_points = \
{'poetry.plugin': ['poetry_auto_version = '
                   'poetry_auto_version.plugin:AutoVersionPlugin']}

setup_kwargs = {
    'name': 'poetry-auto-version',
    'version': '0.0.1',
    'description': 'General Events Manager',
    'long_description': '# Poetry auto version plugin\n',
    'author': 'Wonder',
    'author_email': 'wonderbeyond@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wonderbeyond/poetry-auto-version',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
