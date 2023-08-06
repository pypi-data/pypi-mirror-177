# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynecone',
 'pynecone..templates.app',
 'pynecone.compiler',
 'pynecone.components',
 'pynecone.components.base',
 'pynecone.components.datadisplay',
 'pynecone.components.disclosure',
 'pynecone.components.feedback',
 'pynecone.components.forms',
 'pynecone.components.graphing',
 'pynecone.components.layout',
 'pynecone.components.libs',
 'pynecone.components.media',
 'pynecone.components.navigation',
 'pynecone.components.overlay',
 'pynecone.components.tags',
 'pynecone.components.transitions',
 'pynecone.components.typography',
 'pynecone.middleware']

package_data = \
{'': ['*'],
 'pynecone': ['.templates/assets/*',
              '.templates/web/*',
              '.templates/web/pages/*',
              '.templates/web/utils/*']}

install_requires = \
['fastapi>=0.75.0,<0.76.0',
 'gunicorn>=20.1.0,<21.0.0',
 'plotly>=5.10.0,<6.0.0',
 'pydantic==1.9.0',
 'redis>=4.3.5,<5.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'sqlmodel>=0.0.6,<0.0.7',
 'typer>=0.4.1,<0.5.0',
 'uvicorn>=0.17.6,<0.18.0']

entry_points = \
{'console_scripts': ['pc = pynecone.pc:main']}

setup_kwargs = {
    'name': 'pynecone-io',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Nikhil Rao',
    'author_email': 'nikhil@pynecone.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
