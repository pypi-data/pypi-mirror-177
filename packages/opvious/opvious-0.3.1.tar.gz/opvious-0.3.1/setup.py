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
    'version': '0.3.1',
    'description': 'Opvious Python SDK',
    'long_description': "# Opvious Python SDK  [![CI](https://github.com/opvious/sdk.py/actions/workflows/ci.yml/badge.svg)](https://github.com/mtth/opvious/actions/workflows/ci.yml) [![Pypi badge](https://badge.fury.io/py/opvious.svg)](https://pypi.python.org/pypi/opvious/)\n\nThis package provides a lightweight client for interacting with the [Opvious\nAPI][api]. This SDK's functionality is focused on running attempts; for other\noperations consider the [TypeScript CLI or SDK][cli].\n\n## Quickstart\n\nFirst, install this package and have an API access token handy (these can be\ngenerated [here][token]).\n\n```sh\npip install opvious[aio]\n```\n\nWith these steps out of the way, you are ready to solve any of your optimization\nmodels!\n\n```python\nimport opvious\n\n# Instantiate an API client from an API token\nclient = opvious.Client(TOKEN)\n\n# Assemble inputs for a registered formulation\nbuilder = await client.create_inputs_builder('my-formulation')\n# Add dimensions and parameters...\n\n# Start an attempt\nattempt = await client.start_attempt(builder.build())\n\n# Wait for the attempt to complete\noutcome = await attempt.wait_for_outcome()\n```\n\n[api]: https://www.opvious.io\n[cli]: https://www.opvious.io/sdk.ts\n[token]: https://hub.opvious.io/authorizations\n",
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
