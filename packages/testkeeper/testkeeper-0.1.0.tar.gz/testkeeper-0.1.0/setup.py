# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testkeeper',
 'testkeeper.builtin',
 'testkeeper.exception',
 'testkeeper.mock',
 'testkeeper.module',
 'testkeeper.service',
 'testkeeper.util']

package_data = \
{'': ['*'], 'testkeeper': ['.idea/*', '.idea/inspectionProfiles/*', 'db/*']}

install_requires = \
['ddt>=1.6.0,<2.0.0',
 'flask>=2.2.2,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'psutil>=5.9.4,<6.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0',
 'sqlalchemy>=1.4.43,<2.0.0']

entry_points = \
{'console_scripts': ['TK = testkeeper.client:entry',
                     'TestKeeper = testkeeper.client:entry',
                     'testkeeper = testkeeper.client:entry',
                     'tk = testkeeper.client:entry']}

setup_kwargs = {
    'name': 'testkeeper',
    'version': '0.1.0',
    'description': '用于调度测试任务，观测任务执行进度',
    'long_description': None,
    'author': '成都-阿木木',
    'author_email': '848257135@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
