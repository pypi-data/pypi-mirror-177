# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opvious']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=2.2,<3.0', 'pandas>=1.5,<2.0']

extras_require = \
{'aio': ['aiohttp>=3.8,<4.0']}

setup_kwargs = {
    'name': 'opvious',
    'version': '0.3.0',
    'description': 'Opvious Python SDK',
    'long_description': "# Opvious Python SDK  [![CI](https://github.com/mtth/opvious/actions/workflows/ci.yml/badge.svg)](https://github.com/mtth/opvious/actions/workflows/ci.yml) [![Pypi badge](https://badge.fury.io/py/opvious.svg)](https://pypi.python.org/pypi/opvious/)\n\nThis package provides a lightweight client for interacting with the [Opvious\nAPI][]. This SDK's functionality is focused on running attempts; for other\noperations consider the [TypeScript CLI or SDK][].\n\n## Quickstart\n\nFirst, to install this package:\n\n```sh\npip install opvious[aio]\n```\n\nYou'll then need an API access token. You can generate one at\nhttps://hub.opvious.io/authorizations. Once you have it, you can\ninstantiate a client and call its method:\n\n```python\nimport opvious\n\n# Instantiate an API client\nclient = opvious.Client(TOKEN)\n\n# Assemble problem inputs\nbuilder = await client.create_inputs_builder('my-formulation')\n# Add dimensions and parameters...\n\n# Start an attempt\nattempt = await client.start_attempt(builder.build())\n\n# Wait for the attempt to complete\noutcome = await attempt.wait_for_outcome()\n```\n\n[Opvious API]: https://www.opvious.io/\n[Typescript SDK]: https://www.opvious.io/sdk.ts/\n",
    'author': 'Opvious Engineering',
    'author_email': 'oss@opvious.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/opvious/sdk.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
