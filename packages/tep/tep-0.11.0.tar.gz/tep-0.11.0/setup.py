# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tep']

package_data = \
{'': ['*'],
 'tep': ['template/*',
         'template/examples/*',
         'template/examples/assert/*',
         'template/examples/db/*',
         'template/examples/env_vars/*',
         'template/examples/faker/*',
         'template/examples/func/*',
         'template/examples/http/*',
         'template/examples/login_pay/*',
         'template/examples/login_pay/mvc/*',
         'template/examples/login_pay/mvc/services/*',
         'template/examples/login_pay/tep/*',
         'template/fixtures/*',
         'template/resources/*',
         'template/resources/env_vars/*',
         'template/tests/*',
         'template/utils/*']}

install_requires = \
['allure-pytest>=2.8.16,<3.0.0',
 'allure-python-commons>=2.8.16,<3.0.0',
 'faker>=4.1.1,<5.0.0',
 'fastapi>=0.72.0,<0.73.0',
 'jmespath>=0.9.5,<0.10.0',
 'loguru>=0.4.1,<0.5.0',
 'pydantic>=1.9.0,<2.0.0',
 'pytest-assume>=2.4.2,<3.0.0',
 'pytest>=7.1.1,<8.0.0',
 'pyyaml>=5.4.1,<6.0.0',
 'requests>=2.22.0,<3.0.0',
 'urllib3>=1.25.9,<2.0.0',
 'uvicorn>=0.17.0,<0.18.0']

entry_points = \
{'console_scripts': ['tep = tep.cli:main'],
 'pytest11': ['tep = tep.plugin:Plugin']}

setup_kwargs = {
    'name': 'tep',
    'version': '0.11.0',
    'description': 'tep is a testing tool to help you write pytest more easily. Try Easy Pytest!',
    'long_description': '# tep\n\n`tep`是**T**ry **E**asy **P**ytest的首字母缩写，是一款基于pytest测试框架的测试工具，集成了各种实用的第三方包和优秀的自动化测试设计思想，帮你快速实现自动化项目落地。\n\n官方认证的持续维护教程：\n\n[【最新】tep完整教程帮你突破pytest](https://dongfanger.gitee.io/blog/%E6%B5%8B%E8%AF%95%E5%B7%A5%E5%85%B7/000-%E3%80%90%E6%9C%80%E6%96%B0%E3%80%91tep%E5%AE%8C%E6%95%B4%E6%95%99%E7%A8%8B%E5%B8%AE%E4%BD%A0%E7%AA%81%E7%A0%B4pytest.html)\n\n',
    'author': 'dongfanger',
    'author_email': 'dongfanger@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dongfanger/tep',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
