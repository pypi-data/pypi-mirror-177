# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nile_verifier']

package_data = \
{'': ['*']}

install_requires = \
['cairo-nile>=0.9.0,<0.10.0',
 'click>=8.1.3,<9.0.0',
 'requests>=2.28.1,<3.0.0',
 'yaspin>=2.2.0,<3.0.0']

entry_points = \
{'nile_plugins.cli': ['verify = nile_verifier.main.verify']}

setup_kwargs = {
    'name': 'nile-verifier',
    'version': '0.1.4',
    'description': 'Nile plugin to verify smart contracts on starkscan.co',
    'long_description': '# ⛵️✅ Nile verifier plugin\n\nPlugin for [Nile](https://github.com/OpenZeppelin/nile) to verify contracts on [starkscan.co](https://starkscan.co).\n\n## Installation\n\n```\npip install nile-verifier\n```\n\n## Usage\n\n```\nnile verify CONTRACT_PATH --network NETWORK\n```\n\nFor example:\n```\n$ nile verify contracts/uwu.cairo --network goerli\n🔎 Verifying uwu on goerli...\n✅ Success! https://testnet.starkscan.co/class/0x226718449b40fa299d718eb50f72af707f2210e540e11a830c2ad72a235d5e0#code\n```\n\nNote that the contract has to be deployed, or the verification will fail\n```\n$ nile verify contracts/uwu.cairo --network goerli\n❌ Could not find any contract with hash 0x226718449b40fa299d718eb50f72af707f2210e540e11a830c2ad72a235d5e0\n🤔 Are you sure you deployed to goerli?\n```\n\n## License\n\nMIT.\n\n',
    'author': 'Martín Triay',
    'author_email': 'martriay@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/martriay/nile-verifier-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
