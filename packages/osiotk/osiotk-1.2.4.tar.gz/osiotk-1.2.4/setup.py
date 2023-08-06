# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['osiotk', 'osiotk.path', 'osiotk.scan']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'osiotk',
    'version': '1.2.4',
    'description': 'os io toolkit',
    'long_description': '\n## Osiotk\n\n## Description:\n\n    os io toolkit\n\n',
    'author': 'wayfaring-stranger',
    'author_email': 'zw6p226m@duck.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
