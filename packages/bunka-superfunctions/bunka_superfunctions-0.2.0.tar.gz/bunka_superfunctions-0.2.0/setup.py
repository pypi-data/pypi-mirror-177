# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bunka_superfunctions']

package_data = \
{'': ['*']}

install_requires = \
['community>=1.0.0b1,<2.0.0',
 'dotenv>=0.0.5,<0.0.6',
 'importlib-metadata>=5.0.0,<6.0.0',
 'networkx>=2.8.8,<3.0.0',
 'node2vec>=0.4.6,<0.5.0',
 'pandas>=1.5.1,<2.0.0',
 'plotly>=5.11.0,<6.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'python-louvain>=0.16,<0.17',
 'scikit-learn>=1.1.3,<2.0.0',
 'sklearn>=0.0.post1,<0.1',
 'twine>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'bunka-superfunctions',
    'version': '0.2.0',
    'description': 'some functions often used to do diverse Data Science Projects',
    'long_description': '# local-functions\n\nPrivate repositories from diverse functions used for Data Science\n\npoetry export --without-hashes --format=requirements.txt > requirements.txt\n\n## Build the package\n\npoetry build\npoetry publish -u USERNAME -p PASSWORD\n',
    'author': 'Charles De Dampierre',
    'author_email': 'charles.de-dampierre@hec.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
