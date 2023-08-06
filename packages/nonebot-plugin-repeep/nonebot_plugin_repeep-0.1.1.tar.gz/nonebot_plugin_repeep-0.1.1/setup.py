# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_repeep']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.1.5,<3.0.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0',
 'user-agents>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-repeep',
    'version': '0.1.1',
    'description': 'A plugin based on nonebot2, which is used to display the current peeping user information in QQ.',
    'long_description': '<div align="center">\n  <a href="https://github.com/p0ise/nonebot-plugin-repeep">\n    <img src="logo.png" alt="Logo" width="80" height="80">\n  </a>\n  <h3 align="center">nonebot-plugin-repeep</h3>\n  <p align="center">\n    ✨ 一款基于nonebot2的插件，用于获取QQ中当前窥屏用户信息 ✨\n    <br />\n    <br />\n  \t<a href="https://raw.githubusercontent.com/p0ise/nonebot-plugin-repeep/main/LICENSE">\n    \t<img src="https://img.shields.io/github/license/p0ise/nonebot-plugin-repeep.svg" alt="license">\n  \t</a>\n  \t<a href="https://pypi.python.org/pypi/nonebot-plugin-repeep">\n    \t<img src="https://img.shields.io/pypi/v/nonebot-plugin-repeep.svg" alt="pypi">\n  \t</a>\n  \t<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n  </p>\n</div>\n\n\n\n<!-- TABLE OF CONTENTS -->\n\n<details>\n  <summary>目录</summary>\n  <ol>\n    <li>\n      <a href="#关于">关于</a>\n    </li>\n    <li>\n      <a href="#开始使用">开始使用</a>\n      <ul>\n        <li><a href="#前置条件">前置条件</a></li>\n        <li><a href="#安装">安装</a></li>\n        <li><a href="#配置项">配置项</a></li>\n      </ul>\n    </li>\n    <li><a href="#用法">用法</a></li>\n    <li><a href="#开发计划">开发计划</a></li>\n    <li><a href="#贡献">贡献</a></li>\n    <li><a href="#license">License</a></li>\n    <li><a href="#致谢">致谢</a></li>\n  </ol>\n</details>\n\n# 关于\n\n本项目能够在QQ中获取当前窥屏用户的信息。\n\n> 由于本项目性质，使用的人多了之后检测接口随时会失效，且用且珍惜。\n\n# 开始使用\n\n## 前置条件\n\n- CSRF信息记录后端\n- IP定位接口\n\n### CSRF后端\n\n本项目的CSRF后端需要实现三个接口：\n\n1. 获取Key（用于标识一个会话用于收集CSRF信息）\n2. 渲染图片记录客户端信息\n3. 取出收集到的信息\n\n目前仅支持PHP实现的后端，具体搭建见[repeep-backend-php](https://github.com/p0ise/repeep-backend-php)。\n\n### IP定位接口\n\n目前采用[IPUU](https://mall.ipplus360.com/pros/IPVFourGeoAPI)提供的区县级定位接口，允许每天2000次免费调用，请开发者自行申请后将密钥填入配置项。\n\n## 安装\n\n使用 nb-cli 安装\n\n```sh\nnb plugin install nonebot-plugin-repeep\n```\n\n使用 pip 安装\n\n```sh\npip install nonebot-plugin-repeep\n```\n\n## 配置项\n\n配置方式：直接在 NoneBot 全局配置文件中添加以下配置项即可。\n\n### 必填配置\n\n#### CSRF后端\n\n| 名称         | 类型  | 默认值 | 说明           |\n| ------------ | ----- | ------ | -------------- |\n| trace_secret | `str` | 无     | 后端接口的密钥 |\n| trace_api    | `str` | 无     | 后端接口的URL  |\n\n#### IP定位接口\n\n| 名称      | 类型  | 默认值   | 说明                           |\n| --------- | ----- | -------- | ------------------------------ |\n| geoip_api | `str` | `"ipuu"` | 接口选项，目前仅支持`ipuu`接口 |\n| ipuu_key  | `str` | 无       | `ipuu`接口密钥                 |\n\n### 可选配置\n\n#### XML样式\n\n| 名称    | 类型  | 默认值                                                       | 说明            |\n| ------- | ----- | ------------------------------------------------------------ | --------------- |\n| brief   | `str` | `"I Got U"`                                                  | XML卡片简介     |\n| url     | `str` | `"https://www.p0ise.cn/"`                                    | XML卡片跳转链接 |\n| title   | `str` | `"谁在窥屏"`                                                 | XML卡片标题     |\n| content | `str` | ``"抓住你了！"``                                             | XML卡片内容     |\n| source  | `str` | `"I Got U"`                                                  | XML来源信息     |\n| image   | `str` | `"https://static-cdn.p0ise.cn/2022/11/20221120180503774.jpg"` | XML图片         |\n\n# 用法\n\n- 发送 Command ：`谁在窥屏` 或者 `leakip`\n\n# 开发计划\n\n- [x] 优化IP位置数据精准度\n\n- [ ] 优化信息样式，拟采用HTML渲染输出图片\n- [ ] 增加指令选项，指定获取目标群、用户信息\n- [ ] 优化基于UA的设备识别\n- [ ] 增加对电脑的检测\n- [ ] 智能选择CSRF方法\n\n# 原理\n\n机器人基于python的nonebot2框架，QQ协议基于go-cqhttp。\n\n插件实现原理是QQ的跨站请求伪造。通过图片调起GET方法访问接口，从而获取客户端IP和UA信息。\n\n根据IP，获取定位信息。基于ipuu的在线接口。\n\n根据UA，获取设备信息。基于user_agents库，增加中文优化和型号名称优化。\n\nCSRF原理参考：https://cloud.tencent.com/developer/article/1933686\n\n# 贡献\n\nFork本仓库后进行更改，然后提交PR。\n\n# LICENSE\n\n本项目采用 GPL 3.0 协议。\n\n# 致谢\n\n- [Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp)\n- [nonebot / nonebot2](https://github.com/nonebot/nonebot2)\n- [Y5neKO / qq_xml_ip](https://github.com/Y5neKO/qq_xml_ip)',
    'author': 'p0ise',
    'author_email': 'changelf@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/p0ise/nonebot-plugin-repeep',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
