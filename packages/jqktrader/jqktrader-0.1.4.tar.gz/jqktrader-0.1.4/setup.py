# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jqktrader', 'jqktrader.config', 'jqktrader.utils']

package_data = \
{'': ['*']}

install_requires = \
['easyutils>=0.1.7,<0.2.0',
 'pandas>=1.5.1,<2.0.0',
 'pypiwin32>=223,<224',
 'pytesseract>=0.3.10,<0.4.0',
 'pywinauto>=0.6.8,<0.7.0']

setup_kwargs = {
    'name': 'jqktrader',
    'version': '0.1.4',
    'description': '',
    'long_description': "![qrcode](./qrcode.png)\n# jqktrader\n\n同花顺自动程序化交易\n\n# 目的\n\n由于`easytrader`年久失修，同花顺自动交易模式存在问题，此包基于`easytrader`部分源码，删去其他部分，只专注与同花顺客户端的自动化交易，并解决`easytrader`现存问题，让使用者可以开箱即用。\n\n# 解决的问题\n\n* 升级pywinauto到最新版\n* 补全缺少的依赖，如`pytesseract`、`pypiwin32`\n* 修复无法自动填写输入框的各种问题\n* 增加Tesseract的路径配置\n\n# 安装\n\n## 1. 安装 Tesseract OCR\n\n由于程序运行过程中，需要识别验证码，请首先安装`Tesseract OCR`，官方下载地址：\n\n> https://github.com/UB-Mannheim/tesseract/wiki\n\n## 2. 安装 jqktrader\n\n```\npip install jqktrader\n```\n\n# 用法\n\n> jqktrader不维护同花顺客户端的登录状态，请手动登录后再使用。\n\n```python\nimport jqktrader\n\nuser = jqktrader.use()\n\nuser.connect(\n  exe_path=r'D:\\同花顺软件\\同花顺\\xiadan.exe',\n  tesseract_cmd=r'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'\n)\n\nuser.position\n```\n\n**exe_path** 同花顺`xiadan.exe`的路径\n\n**tesseract_cmd** Tesseract OCR `tesseract.exe`的路径\n\n# API\n\n沿用easyTrader官方的api，非同花顺相关的已删除。\n\n参看文档：https://easytrader.readthedocs.io/zh/master/usage/\n\n",
    'author': 'pluto',
    'author_email': 'mayuanchi1029@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
