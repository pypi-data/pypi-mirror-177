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
    'version': '0.0.1',
    'description': 'Liquidswap Python SDK',
    'long_description': '# liquidswap-sdk-python\n\nWIP:\n\n- [x] convert_to_decimals\n- [x] calculate_rates\n- [x] swap\n- [ ] create pypl package\n\n',
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
