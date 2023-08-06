# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tidify']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'tidify',
    'version': '0.1.2',
    'description': 'Convert nested objects into tidy data',
    'long_description': '# `tidify`: Convert nested objects into tidy data\n\n[![Build Status](https://cloud.drone.io/api/badges/tangibleintelligence/tidify/status.svg)](https://cloud.drone.io/tangibleintelligence/tidify)\n[![PyPI version](https://badge.fury.io/py/tidify.svg)](https://badge.fury.io/py/tidify)\n\nThis package allows for simple conversion of arbitrarily nested data (of objects and arrays) into a format akin to\n[Tidy Data](https://vita.had.co.nz/papers/tidy-data.pdf).\n\nArrays are expanded to multiple rows, with a new `.index` column created. Nested objects are expanded into multiple\ncolumns with `.` (or customizable) separator.',
    'author': 'Austin Howard',
    'author_email': 'austin@tangibleintelligence.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tangibleintelligence/tidify',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
