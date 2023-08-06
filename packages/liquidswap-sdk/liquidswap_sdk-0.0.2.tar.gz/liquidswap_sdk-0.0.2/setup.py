# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['liquidswap_sdk']

package_data = \
{'': ['*']}

install_requires = \
['aptos-sdk>=0.4.1']

setup_kwargs = {
    'name': 'liquidswap-sdk',
    'version': '0.0.2',
    'description': 'Liquidswap Python SDK',
    'long_description': '# liquidswap-sdk-python\n\n\n## Install\nhttps://pypi.org/project/liquidswap-sdk/\n`pip install liquidswap-sdk`\n\n## Functions\n\nimport\n`from liquidswap_sdk.client import LiquidSwapClient`\n\nnew a client\n`liquidswap_client = LiquidSwapClient(node_url, tokens_mapping, wallet_path)`\n\nget the output amount from given input amount\n`liquidswap_client.calculate_rates("APTOS", "USDT", 1)`\n\nswap token\n`liquidswap_client.swap("APTOS", "USDT", 1, usdt_out)`\n\nget token balance\n`liquidswap_client.get_token_balance("APTOS")`\n\nregister token\n`liquidswap_client.register("USDT")`\n\n\n## How to use\n\n1. create your [config](config.py)\n\n2. add token addresses you want to trade to `tokens_mapping`\n\n3. make sure there is some APT in your wallet of `wallet_path`\n\n4. make yout own script! (check: [example](example.py))\n\n5. if you are ready to `mainnt`, change the `node_url` to `https://fullnode.mainnet.aptoslabs.com/v1`\n\n\n## WIP:\n\n- [x] convert_to_decimals\n- [x] calculate_rates\n- [x] swap\n- [x] create pypl package\n\n\n',
    'author': 'Wayne Kuo',
    'author_email': 'wayne01213@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/WayneAl/liquidswap-sdk-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
