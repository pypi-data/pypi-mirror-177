# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['near_seed_phrase', 'near_seed_phrase.utils']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.1,<3.0.0', 'ed25519>=1.5,<2.0', 'mnemonic>=0.20,<0.21']

setup_kwargs = {
    'name': 'near-seed-phrase-py',
    'version': '0.1.0',
    'description': 'Python tool for creating and converting mnemonic-phrases, public key and private key for NEAR accounts.',
    'long_description': '# NEAR Seed Phrase\n\nPython tool for creating and converting mnemonic-phrases, public key and private key for NEAR accounts.\n\n### 🚨 Status: BETA, contributions welcome!\n\n#### Ported to Python from https://github.com/near/near-seed-phrase\n### Install\n\n```py\npoetry add near-seed-phrase-py\n```\n\n```py\npoetry shell\npoetry show -v # copy this virtualenv path and set it as your Python interpreter \npoetry install\n```\n\n### Usage\n```py\n# Generate a BIP39 seed phrase with its corresponding Keys\ngenerate_seed_phrase()\n\nReturns:\n\n{\n    seed_phrase: str # BIP39 seed phrase\n    secret_key: str # ed25519 secret/private key, formatted for NEAR (e.g. "ed25519:[SECRET_KEY]")\n    public_key: str # ed25519 public key, formatted for NEAR (e.g. "ed25519:[PUBLIC_KEY]")\n    public_key_hex: str # lowercase hex representation of public_key that can be used as an implicit account ID; see https://docs.near.org/integrator/implicit-accounts\n} \n\n# Recover keys from a BIP39 seed phrase (returns same response as generate_seed_phrase())\nparse_seed_phrase(seed_phrase)\n\n```\n\n\n\n\n',
    'author': 'Lachlan Glen',
    'author_email': 'lachlanjglen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lachlanglen/near-seed-phrase-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
