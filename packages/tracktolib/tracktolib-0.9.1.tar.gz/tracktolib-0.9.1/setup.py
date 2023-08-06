# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tracktolib', 'tracktolib.s3']

package_data = \
{'': ['*']}

extras_require = \
{'api': ['fastapi>=0.87.0,<0.88.0'],
 'http': ['httpx>=0.23.0,<0.24.0'],
 'logs': ['python-json-logger>=2.0.4,<3.0.0'],
 'pg-sync': ['psycopg2>=2.9.5,<3.0.0'],
 's3': ['aiobotocore>=2.4.0,<3.0.0'],
 's3-minio': ['minio>=7.1.12,<8.0.0'],
 'tests': ['deepdiff>=6.2.1,<7.0.0']}

setup_kwargs = {
    'name': 'tracktolib',
    'version': '0.9.1',
    'description': 'Utility library for python',
    'long_description': '# Tracktolib\n\n[![Python versions](https://img.shields.io/pypi/pyversions/tracktolib)](https://pypi.python.org/pypi/tracktolib)\n[![Latest PyPI version](https://img.shields.io/pypi/v/tracktolib?logo=pypi)](https://pypi.python.org/pypi/tracktolib)\n[![CircleCI](https://circleci.com/gh/Tracktor/tracktolib/tree/master.svg?style=shield)](https://app.circleci.com/pipelines/github/Tracktor/tracktolib?branch=master)\n\nUtility library for python\n\n# Installation\n\nYou can choose to not install all the dependencies by specifying\nthe [extra](https://python-poetry.org/docs/cli/#options-4) parameter such as:\n\n```bash\npoetry add tracktolib@latest -E pg-sync -E tests --group dev \n```\n\nHere we only install the utilities using `psycopg2` (pg-sync) and `deepdiff` (tests) for the dev environment.\n\n# Utilities\n\n- **pg-sync**\n\nUtility functions based on psycopg2 such as `fetch_one`, `insert_many`, `fetch_count` ...\n\n- **tests**\n\nUtility functions for tests such as `get_uuid` (that generates a test uuid based on an integer)\n\n- **s3-minio**\n\nUtility functions for [minio](https://min.io/docs/minio/linux/developers/python/API.html)\n\n- **s3**\n\nUtility functions for [aiobotocore](https://github.com/aio-libs/aiobotocore)\n\n- **logs**\n\nUtility functions to initialize the logging formatting and streams\n\n- **http**\n\nUtility functions using [httpx](https://www.python-httpx.org/)\n\n- **api**\n\nUtility functions using [fastapi](https://fastapi.tiangolo.com/)\n',
    'author': 'Julien Brayere',
    'author_email': 'julien.brayere@tracktor.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tracktor/tracktolib',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
