# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['http_client_sync']
install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'http-client-sync',
    'version': '0.1.0',
    'description': 'Http Client for work with API.',
    'long_description': '# HttpApiGather\nSimple Http client for convenient work with api.',
    'author': 'Alexandr Kolesnikov',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
