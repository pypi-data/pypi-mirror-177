# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydra', 'pydra.tasks.bids', 'pydra.tasks.bids.tests']

package_data = \
{'': ['*']}

install_requires = \
['ancpbids>=0.2.1,<0.3.0', 'pydra>=0.20,<0.21']

setup_kwargs = {
    'name': 'pydra-bids',
    'version': '0.0.4',
    'description': 'Pydra tasks for BIDS I/O',
    'long_description': "# pydra-bids\n\nPydra tasks for BIDS I/O.\n\n[Pydra] is a dataflow engine which provides a set of lightweight abstractions\nfor DAG construction, manipulation, and distributed execution.\n\n[BIDS] defines standards for organizing neuroimaging files and metadata.\n\nThis project provides tasks for reading from and writing to BIDS datasets.\n\n## Development\n\nThis project is managed using [Poetry].\n\nTo install, check and test the code:\n\n```console\nmake\n```\n\nTo run the test suite when hacking:\n\n```console\nmake test\n```\n\nTo format the code before review:\n\n```console\nmake format\n```\n\nTo build the project's documentation:\n\n```console\nmake docs\n```\n\n## Licensing\n\nThis project is released under the terms of the Apache License 2.0.\n\n[Pydra]: https://nipype.github.io/pydra\n[BIDS]: https://bids-specification.readthedocs.io\n[Poetry]: https://python-poetry.org\n",
    'author': 'The Aramis Lab',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aramis-lab/pydra-bids',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
