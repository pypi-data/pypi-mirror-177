# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['secrets_env', 'secrets_env.auth', 'secrets_env.cli', 'secrets_env.config']

package_data = \
{'': ['*'], 'secrets_env': ['templates/*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'httpx[http2]>=0.23.1,<0.24.0']

extras_require = \
{'all': ['keyring>=23.3.0,<24.0.0', 'PyYAML>=5.1.2,<7'],
 'all:python_version < "3.11"': ['tomli>=1.1.0,<3'],
 'keyring': ['keyring>=23.3.0,<24.0.0'],
 'toml:python_version < "3.11"': ['tomli>=1.1.0,<3'],
 'yaml': ['PyYAML>=5.1.2,<7']}

entry_points = \
{'console_scripts': ['secrets.env = secrets_env.cli:main'],
 'poetry.application.plugin': ['poetry-secrets-env-plugin = '
                               'secrets_env.poetry:SecretsEnvPlugin']}

setup_kwargs = {
    'name': 'secrets-env',
    'version': '0.20.0',
    'description': 'Put secrets from Vault to environment variables',
    'long_description': "Secrets.env\n===========\n\nPut secrets from `Vault <https://www.vaultproject.io/>`_ KV engine to environment variables like a ``.env`` loader, without landing data on disk.\n\n.. code-block:: bash\n\n   $ cat .secrets-env.yaml\n   source:\n     url: http://localhost:8200\n     auth: token\n\n   secrets:\n     EXAMPLE:\n       path: secrets/example\n       field: foo\n\n   $ secrets.env run sh -c 'echo \\$EXAMPLE = $EXAMPLE'\n   [secrets_env] Read secrets.env config from /Users/tim_shih/.secrets-env.yaml\n   [secrets_env] 🔑 1 secrets loaded\n   $EXAMPLE = hello\n\nSecurity is important, but don't want it to be a stumbling block. We love secret manager, but the practice of getting secrets for local development could be a trouble.\n\nThis app is built to *plug in* secrets into development without landing data on disk, easily reproduce the environment, and reduce the risk of uploading the secrets to the server.\n",
    'author': 'tzing',
    'author_email': 'tzingshih@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tzing/secrets.env',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
