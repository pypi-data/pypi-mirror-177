# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nasbio', 'nasbio.app', 'nasbio.db']

package_data = \
{'': ['*']}

install_requires = \
['celery>=5.2.7,<6.0.0',
 'fastapi>=0.86.0,<0.87.0',
 'sqlalchemy>=1.4.43,<2.0.0',
 'strawberry-graphql[fastapi]>=0.140.0,<0.141.0',
 'uvicorn[standard]>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'nasbio',
    'version': '0.1.12',
    'description': '',
    'long_description': '# NASBio Web Services\n## Common Python Packages\n',
    'author': 'Kah Wai LIM',
    'author_email': 'kahwai222@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
