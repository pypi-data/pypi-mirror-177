# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rockydb']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.85.1,<0.86.0',
 'pytest>=7.2.0,<8.0.0',
 'rocksdict==0.3.2',
 'uvicorn>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'rockydb',
    'version': '0.2.10',
    'description': 'A NoSQL database.',
    'long_description': '# RockyDB \n[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n![CI](https://github.com/aaldulimi/rockydb/actions/workflows/integrate.yml/badge.svg)\n[![codecov](https://codecov.io/github/aaldulimi/RockyDB/branch/master/graph/badge.svg?token=6MZLCKX5IJ)](https://codecov.io/github/aaldulimi/RockyDB)\n\nSimple NoSQL database written in Python. It relies on rocksdb as its storage engine. This is more of a Proof-of-concept than a production-ready database. \n\n## Installation \n```\npip install rockydb\n```\n\n## Contents\n- [RockyDB](#rockydb)\n- [Installation](#installation)\n- [Contents](#contents)\n- [Features](#features)\n- [Documentation](#documentation)\n    - [Create collection](#create-collection)\n    - [Insert doucment](#insert-document)\n    - [Get document](#get-document)\n    - [Delete document](#delete-document)\n    - [Query](#query)\n    \n\n\n## Features\nCurrently under active development, however here is the feature list so far:\n\n- **Create collections**\n- **Insert, get and delete documents**\n- **REST API**\n- **Query language**\n- **Indexes**\n- **Full-text Search [IN-DEVELOPMENT]**\n\n## Performance\nDataset: [NBA Players Dataset](https://www.kaggle.com/datasets/drgilermo/nba-players-stats).\nComputer: MacBook Pro (13-inch, 2019).\nRockyDB is still in its early days, these results will likely get better in the future. \n| Database      | Insert | Get | Query | Delete \n| -----------| -----------:| -----------:| -----------:| -----------:| \n| RockyDB      | **0.00074**       | **0.00038** | 0.00014 | **0.00023**\n| MongoDB   | 0.04436        | 0.04518 | **0.00004**  | 0.04264\n\n## Documentation\nFull [Documentation](https://rockydb.readthedocs.io/en/latest/). Below are the basics:\n### Create collection \n```python\nfrom rockydb import RockyDB\n\ndb = RockyDB(path="database/")\nnews = db.collection("news")\n```\n\n### Insert document\nSupported data types: `str`, `int`, `float`, `bool` and `list`. Will support more later. \n```python\ndoc_id = news.insert({\n  "title": "Can store strings",\n  "year": 2022,\n  "people": ["lists", "are", "fine", "too"],\n  "pi": 3.14,\n  "real": True\n})\n```\nThe `insert` method will return a unique document `_id`. `_id` will be created if document does not contain it.  \n\n### Get document\n```python\nnews.get(doc_id)\n```\n### Delete document\n```python\nnews.delete(doc_id)\n```\n### Query\n```python\nnews.find({"pi?lt": 3.14, "real": True}, limit=10)\n``` \nThe `limit` arg is optional, default is 10. Supports exact, lte, lt, gt and gte queries.\n',
    'author': 'Ahmed',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aaldulimi/RockyDB',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
