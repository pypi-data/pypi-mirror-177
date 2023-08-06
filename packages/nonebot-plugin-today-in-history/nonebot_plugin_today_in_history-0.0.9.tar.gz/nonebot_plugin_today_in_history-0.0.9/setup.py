# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_today_in_history']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0',
 'nonebot-adapter-onebot>=2.1.1,<3.0.0',
 'nonebot-plugin-apscheduler>=0.1.2,<0.2.0',
 'nonebot-plugin-htmlrender>=0.2.0,<0.3.0',
 'nonebot2>=2.0.0b4,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-today-in-history',
    'version': '0.0.9',
    'description': 'Send Today In History to friends or group chat',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-today-in-history\n\n_✨ 历史上的今天 ✨_\n\n\n<a href="./LICENSE">\n    <img src="https://img.shields.io/github/license/AquamarineCyan/nonebot-plugin-today-in-history.svg" alt="license">\n</a>\n<a href="https://pypi.python.org/pypi/nonebot-plugin-today-in-history">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-today-in-history.svg" alt="pypi">\n</a>\n<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">\n\n</div>\n\n## 📖 介绍\n\n定时向指定群&好友发送  **历史上的今天**\n\n数据源：[历史上的今天-百度百科](https://baike.baidu.com/calendar/)\n\n鸣谢 [bingganhe123/60s-](https://github.com/bingganhe123/60s-) ~~进行一个简单的抄~~\n\n**推荐python`3.9+`\n\n## 💿 安装\n\n<details>\n<summary>使用 nb-cli 安装</summary>\n在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装\n\n    nb plugin install nonebot-plugin-today-in-history\n\n</details>\n\n<details>\n<summary>使用包管理器安装</summary>\n在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令\n\n    pip install nonebot-plugin-today-in-history\n\n\n打开 nonebot2 项目的 `bot.py` 文件, 在其中写入\n\n    nonebot.load_plugin(\'nonebot_plugin_today_in_history\')\n\n</details>\n\n<details>\n<summary>从 github 安装</summary>\n在 nonebot2 项目的插件目录下, 打开命令行, 输入以下命令克隆此储存库\n\n    git clone https://github.com/AquamarineCyan/nonebot-plugin-today-in-history.git\n\n打开 nonebot2 项目的 `bot.py` 文件, 在其中写入\n\n    nonebot.load_plugin(\'src.plugins.nonebot_plugin_today-in-history\')\n\n</details>\n\n## ⚙️ 配置\n\n在 nonebot2 项目的`.env`文件中添加以下配置\n\n新版配置，`v0.0.9`及以上\n\n```\n# nonebot-plugin-today-in-history\nhistory_qq_friends=[123456789,123456789] #设定要发送的QQ好友\nhistory_qq_groups=[123456789,123456789,123456789] #设定要发送的群\nhistory_inform_time="7 35" #设定每天发送时间，以空格间隔\n```\n<details>\n<summary>旧版配置，`v0.0.8`及以下</summary>\n\n```\n#nonebot-plugin-today-in-history\nhistory_qq_friends=[12345678910] #设定要发送的QQ好友\nhistory_qq_groups=[123456789,123456789,123456789] #设定要发送的群\nhistory_inform_time=[{"HOUR":9,"MINUTE":1}] #在输入时间的时候 不要 以0开头如{"HOUR":06,"MINUTE":08}是错误的\n```\n</details>\n\n\n\n## 🎉 使用\n\n- 发送 `历史上的今天`\n\n    > 完全匹配 `历史上的今天`\n\n- 定时任务，`.env`配置发送好友、群、时间\n\n### 效果图\n\n![img.png](img.png)\n',
    'author': 'AquamarineCyan',
    'author_email': '1057424730@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
