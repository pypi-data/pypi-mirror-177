# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nth']

package_data = \
{'': ['*']}

extras_require = \
{'cli': ['python-dotenv>=0.20.0,<0.21.0']}

entry_points = \
{'console_scripts': ['nth = nth.__main__:main']}

setup_kwargs = {
    'name': 'nth',
    'version': '0.1.8',
    'description': '',
    'long_description': 'None',
    'author': 'Nils Olsson',
    'author_email': 'nilso@enosis.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
