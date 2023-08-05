# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evervault',
 'evervault.crypto',
 'evervault.crypto.curves',
 'evervault.datatypes',
 'evervault.errors',
 'evervault.http',
 'evervault.models',
 'evervault.services']

package_data = \
{'': ['*']}

install_requires = \
['certifi',
 'cryptography>=3.4.8,<4.0.0',
 'pyasn1>=0.4.8,<0.5.0',
 'pycryptodome>=3.10.1,<4.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'evervault',
    'version': '1.3.3',
    'description': 'Evervault SDK',
    'long_description': "[![Evervault](https://evervault.com/evervault.svg)](https://evervault.com/)\n\n[![Unit Tests Status](https://github.com/evervault/evervault-python/workflows/evervault-unit-tests/badge.svg)](https://github.com/evervault/evervault-python/actions?query=workflow%3Aevervault-unit-tests)\n\n# Evervault Python SDK\n\nThe [Evervault](https://evervault.com) Python SDK is a toolkit for encrypting data as it enters your server, working with Cages, and proxying your outbound api requests to specific domains through [Outbound Relay](https://docs.evervault.com/concepts/relay/outbound-interception) to allow them to be decrypted before reaching their target.\n\n## Getting Started\n\nBefore starting with the Evervault Python SDK, you will need to [create an account](https://app.evervault.com/register) and a team.\n\nFor full installation support, [book time here](https://calendly.com/evervault/cages-onboarding).\n\nBefore contributing, make sure to use [commitizen](https://github.com/commitizen/cz-cli) & to read [Contributing.md](./CONTRIBUTING.md).\n\n## Documentation\n\nSee the Evervault [Python SDK documentation](https://docs.evervault.com/sdk/python).\n\n## Installation\n\nOur Python SDK is distributed via [pypi](https://pypi.org/project/evervault/), and can be installed using `pip`.\n\n```sh\npip install evervault\n```\n\n## Setup\n\nTo make Evervault available for use in your app:\n\n```python\nimport evervault\n\n# Initialize the client with your team's api key\nevervault.init('<YOUR-API-KEY>')\n\n# Encrypt your data and run a cage\nresult = evervault.encrypt_and_run(<CAGE-NAME>, { 'hello': 'World!' })\n```\n\n## Reference\n\nThe Evervault Python SDK exposes five functions.\n\n### evervault.init()\n\n`evervault.init()` initializes the SDK with your API key. Configurations for the interception of outbound requests may also be passed in this function.\n\n```python\nevervault.init(api_key = str[, decryption_domains=[], retry = bool, curve = str])\n```\n\n| Parameter      | Type        | Description                                                              |\n| -------------- | ----------- | ------------------------------------------------------------------------ |\n| api_key        | `str`       | The API key of your Evervault Team                                       |\n| decryption_domains      | `list(str)` | Requests sent to any of the domains listed will be proxied with Outbound Interception. Wildcard domains are supported. See [Outbound Relay](/concepts/relay/outbound-interception) to learn more. |\n| enable_outbound_relay **(beta)** | `bool` | Enabling this flag will configure Outbound Relay and intercept requests to domains configured in the Evervault UI. |\n| retry          | `bool`      | Retry failed Cage operations (maximum of 3 retries; `false` by default)  |\n| curve          | `str`       | The elliptic curve used for cryptographic operations. See [Elliptic Curve Support](https://docs.evervault.com/reference/elliptic-curve-support) to learn more. |\n| debugRequests  | `bool`      | Output request domains and whether they were sent through outbound proxy |\n\n### evervault.encrypt()\n\n`evervault.encrypt()` encrypts data for use in your [Cages](https://docs.evervault.com/tutorial). To encrypt data at the server, simply pass a python primitive type into the `evervault.encrypt()` function. Store the encrypted data in your database as normal.\n\n```python\nevervault.encrypt(data = dict | list | set | str | int | bool)\n```\n\n| Parameter | Type                                        | Description          |\n| --------- | ------------------------------------------- | -------------------- |\n| data      | `dict`, `list`, `set`, `str`, `int`, `bool` | Data to be encrypted |\n\n### evervault.run()\n\n`evervault.run()` invokes a Cage with a given payload.\n\n```python\nevervault.run(cage_name = str, data = dict[, options = dict])\n```\n\n| Parameter | Type   | Description                                    |\n| --------- | ------ | ---------------------------------------------- |\n| cage_name | `str`  | Name of the Cage to be run.                    |\n| data      | `dict` | Payload for the Cage.                          |\n| options   | `dict` | [Options for the Cage run.](#Cage-Run-Options) |\n\n#### Cage Run Options\n\n| Option  | Type      | Default | Description                                                                          |\n| ------- | --------- | ------- | ------------------------------------------------------------------------------------ |\n| async   | `Boolean` | `False` | Run your Cage in async mode. Async Cage runs will be queued for processing.          |\n| version | `Integer` | `None`  | Specify the version of your Cage to run. By default, the latest version will be run. |\n\n### evervault.create_run_token()\n\n`evervault.create_run_token()` creates a single use, time bound token for invoking a cage.\n\n```python\nevervault.create_run_token(cage_name = str, data = dict)\n```\n\n| Parameter | Type   | Description                                           |\n| --------- | ------ | ----------------------------------------------------- |\n| cage_name | `str`  | Name of the Cage the run token should be created for. |\n| data      | `dict` | Payload that the token can be used with.              |\n\n## Contributing\n\nBug reports and pull requests are welcome on GitHub at https://github.com/evervault/evervault-python.\n\n## Feedback\n\nQuestions or feedback? [Let us know](mailto:support@evervault.com).\n",
    'author': 'Evervault',
    'author_email': 'engineering@evervault.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://evervault.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
