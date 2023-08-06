# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mini_six',
 'mini_six.core',
 'mini_six.portable',
 'mini_six.portable.win32',
 'mini_six.portable.win32.operation']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.21.6', 'opencv-python==4.4.0.46']

setup_kwargs = {
    'name': 'mini-six',
    'version': '0.1.5',
    'description': 'A cross-platform, highly scalable, maintainable, machine-aware, machine-aware, limited state machine framework.',
    'long_description': '# SIX\n![image](https://img.shields.io/badge/python-3.7-blue)\n![image](https://img.shields.io/badge/opencv-4.4.0.46-brightgreen)\n![image](https://img.shields.io/badge/numpy-1.21-red)\n![image](https://img.shields.io/badge/windows-10-informational)\n## 这是什么\nSIX 是一个跨平台的、可扩展性高、可维护性强的基于机器感知的有限状态机框架。本项目原则为“精简至上”，尽量使用python原生库以保证本项目的可扩展性。\n## 安装\n```shell\npip install mini-six\n```\n## 使用\n本项目提供插件开发接口，详细操作请见[操作文档](doc/manual-zh-cn.md)。\n## 开发任务\n因为该项目仍处在起步阶段，所以必要时候会对框架做出调整，作者会尽量以兼容的形式做出这些必要的调整。\n### core（当前主要开发任务）\n- [x] 完成 Observer 和 Actor 的订阅者框架搭建，将图片帧的输入与对图片的操作解耦；\n- [x] 完成 Analyzer 基类的构建，使开发者专注对图片帧的分析操作，增加分析代码的复用度；\n- [x] 优化订阅者框架的接口，方便插件开发者定义 Action；\n- [x] 删除 Analyzer，简化 core 代码，同时增加插件开发者的开发自由度；\n- [x] 构建全局配置和局部配置系统\n- [x] 构建插件系统\n- [x] 优化插件导入接口\n- [x] 实现定时 Action\n- [x] 实现静态配置设置与导入接口\n- [x] 增加日志打印\n- [x] 编写操作文档\n- [ ] 适配 Linux 平台\n- [ ] 适配嵌入式设备\n### plugin（陆续开发）\n- [ ] 图像识别模型接口插件\n- [ ] 强化学习模型接口插件',
    'author': 'TsangHans',
    'author_email': 'gzzenghan@189.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Six-Project/six.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
