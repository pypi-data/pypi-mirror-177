# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vector_search_api',
 'vector_search_api.exceptions',
 'vector_search_api.helper',
 'vector_search_api.schema',
 'vector_search_api.search']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.0.0,<2.0.0']

extras_require = \
{'all': ['faiss-cpu>=1.0.0,<2.0.0', 'pinecone-client>=2.0.0,<3.0.0'],
 'faiss': ['faiss-cpu>=1.0.0,<2.0.0'],
 'pinecone': ['pinecone-client>=2.0.0,<3.0.0']}

setup_kwargs = {
    'name': 'vector-search-api',
    'version': '0.4.2',
    'description': 'Vector-Search API of databases.',
    'long_description': 'None',
    'author': 'AllenChou',
    'author_email': 'f1470891079@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
