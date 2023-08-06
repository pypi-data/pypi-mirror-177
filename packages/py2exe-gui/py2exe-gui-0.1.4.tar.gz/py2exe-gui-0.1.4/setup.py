# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py2exe_gui', 'py2exe_gui.Constants', 'py2exe_gui.Core', 'py2exe_gui.Widgets']

package_data = \
{'': ['*'], 'py2exe_gui': ['Resources/*', 'Resources/Icons/*']}

install_requires = \
['PySide6>=6.2.0,<6.3.0']

setup_kwargs = {
    'name': 'py2exe-gui',
    'version': '0.1.4',
    'description': 'GUI for PyInstaller, based on PySide6',
    'long_description': '![Py2exe-GUI Logo](docs/source/images/py2exe-gui_logo_big.png)\n\n<h2 align="center">强大易用的 Python 图形界面打包工具</h2>\n\n<p align="center">\n<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/muziing/Py2exe-GUI">\n<img alt="Python Version" src="https://img.shields.io/pypi/pyversions/py2exe-gui">\n<a href="https://pypi.org/project/py2exe-gui/"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/py2exe-gui"></a>\n<a href="https://doc.qt.io/qtforpython/index.html"><img alt="PySide Version" src="https://img.shields.io/badge/PySide-6.2-blue"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n<a href="http://mypy-lang.org/"><img alt="Checked with mypy" src="http://www.mypy-lang.org/static/mypy_badge.svg"></a>\n</p>\n\n## 简介\n\nPy2exe-GUI 是一个基于 [PySide6](https://doc.qt.io/qtforpython/index.html) 开发的 [PyInstaller](https://pyinstaller.org/) 辅助工具，旨在提供完整易用的图形化界面，方便用户进行 Python 项目的打包。\n\n![截图](docs/source/images/Py2exe-GUI_v0.1.0_screenshot.png)\n\n有如下特性：\n\n- 完全图形化界面，易用\n- 支持 PyInstaller 的全部选项\n- （暂未实现）可以调用本地任一 Python 解释器，无需在每个待打包的解释器环境中重复安装\n- 可以显式指定打包时使用的 Python 解释器与对应环境（调用该解释器的 `python3 -m PyInstaller myscript.py` 即可）\n- 跨平台，支持 Windows、Linux、MacOS\n\n## 如何使用\n\n> 注意：Py2exe-GUI 尚处早期开发阶段，使用方式可能频繁变化，注意经常查阅此使用说明。\n\n### 方式1：通过 `pip` 安装\n\n首先在待打包的 Python 解释器环境中安装 PyInstaller:\n\n```shell\npip install pyinstaller==5.5\n```\n\n然后通过 pip 安装 Py2exe-GUI：\n\n```shell\npip install py2exe-gui\n```\n\n运行\n\n```shell\npython -m py2exe_gui\n```\n\n### 方式2：通过仓库源码运行\n\n克隆仓库：\n\n```shell\ngit clone https://github.com/muziing/Py2exe-GUI.git\n```\n\n安装依赖项（需要提前安装好 [Poetry](https://python-poetry.org/)）：\n\n```shell\npoetry install\n```\n\n运行 src 目录下的 [Py2exe-GUI.py](src/Py2exe-GUI.py):\n\n```shell\ncd src\npython  Py2exe-GUI.py\n```\n\n\n## 项目结构\n\n- 项目所有代码均在 [py2exe_gui](src/py2exe_gui) 目录下\n- [Widgets](src/py2exe_gui/Widgets) 包包含所有界面控件\n- [Core](src/py2exe_gui/Core) 包用于执行打包\n- [Constants](src/py2exe_gui/Constants) 中为常量\n\n## TODO\n\n- [x] 解决相对引用与作为包运行问题\n- [x] 选项参数获取\n  - [x] 将参数拼接成完整调用命令\n  - [x] 参数预览器控件\n  - [ ] 优化拼接代码\n- [x] 调用 `PyInstaller` 子进程\n  - [x] 使用 `QProcess` 替代 `subprocess` 以解决界面卡死问题\n  - [x] 将子进程的输出与状态显示至单独的弹出窗口\n  - [x] 为 `SubProcessDlg` 增加多功能按钮\n  - [ ] 优化子进程相关代码，增强异常处理\n- [ ] 增加主界面功能控件\n  - [ ] 资源文件添加框\n  - [ ] Python 解释器选择器\n  - [x] 增加状态栏信息\n  - [ ] 「简洁模式」/「详尽模式」切换\n- [ ] 菜单栏功能\n  - [ ] `PyInstaller` 选项参数详解表格\n  - [ ] 打包任务读写\n- [x] 实现跨平台功能\n  - [x] 获取当前运行平台\n  - [x] 以合理方式保存至某种全局变量中\n  - [x] 定制各平台特有功能\n- [ ] 打包任务\n  - [x] 创建打包任务，保存所有选项\n  - [ ] ~~定义文件并以适当格式存储（`json`）~~\n  - [ ] 创建 [`.spec` 文件](https://pyinstaller.org/en/stable/spec-files.html)\n  - [ ] `spec` 编辑器\n- [ ] 使用qrc管理[静态资源](src/py2exe_gui/Resources)\n- [ ] `logging` 日志记录\n- [ ] QSS 与美化\n- [ ] 动画效果\n- [ ] 翻译与国际化\n',
    'author': 'muzing',
    'author_email': 'muzi2001@foxmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/muziing/Py2exe-GUI',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
