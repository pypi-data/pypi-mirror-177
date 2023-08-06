# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hdl21schematicimporter']

package_data = \
{'': ['*']}

install_requires = \
['hdl21>=2.0', 'pydantic>=1.9.1']

setup_kwargs = {
    'name': 'hdl21schematicimporter',
    'version': '1.0.dev0',
    'description': 'Hdl21 Schematics Python Importer',
    'long_description': None,
    'author': 'Dan Fritchman',
    'author_email': 'dan@fritch.mn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
