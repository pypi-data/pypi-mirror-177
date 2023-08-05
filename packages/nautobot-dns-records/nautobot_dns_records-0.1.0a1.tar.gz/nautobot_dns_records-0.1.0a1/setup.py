# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_dns_records',
 'nautobot_dns_records.migrations',
 'nautobot_dns_records.tests',
 'nautobot_dns_records.views']

package_data = \
{'': ['*'], 'nautobot_dns_records': ['templates/nautobot_dns_records/*']}

setup_kwargs = {
    'name': 'nautobot-dns-records',
    'version': '0.1.0a1',
    'description': 'Manage DNS Records in Nautobot',
    'long_description': 'None',
    'author': 'Daniel Bacher',
    'author_email': 'bacher@kit.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
