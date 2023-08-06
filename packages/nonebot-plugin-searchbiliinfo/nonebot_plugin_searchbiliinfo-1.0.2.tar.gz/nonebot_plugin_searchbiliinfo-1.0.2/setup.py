# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_searchbiliinfo']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.1.3,<3.0.0',
 'nonebot-plugin-htmlrender>=0.2.0.1,<0.3.0.0',
 'nonebot2>=2.0.0b5,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-searchbiliinfo',
    'version': '1.0.2',
    'description': 'A plugin for nonebot2. Query Bilibili user information（一个Nonebot2的插件，b站用户信息查询插件【粉丝、舰团信息；直播收益数据；直播观看信息；关键词搜昵称、UID等】）',
    'long_description': '<div align="center">\n\n# nonebot_plugin_searchBiliInfo\n  \n_✨ NoneBot b站用户信息查询插件 ✨_\n  \n\n<a href="./LICENSE">\n    <img src="https://img.shields.io/github/license/tkgs0/nonebot-plugin-antiinsult.svg" alt="license">\n</a>\n<a href="https://pypi.python.org/pypi/nonebot_plugin_searchBiliInfo">\n    <img src="https://img.shields.io/pypi/v/nonebot_plugin_searchBiliInfo.svg" alt="pypi">\n</a>\n<a href="https://www.python.org">\n    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n</a>\n\n</div>\n\n适用于nonebot2 v11的b站用户信息查询插件【粉丝、舰团信息；直播收益数据；直播观看信息；关键词搜昵称、UID等】  \n（ps：微调源码可以兼容其他版本）   \n调用的相关API源自b站官方接口和danmaku.suki.club\n\n## 🔧 开发环境\nNonebot2：2.0.0b5  \npython：3.8.13  \n操作系统：Windows10（CentOS7下正常运行，Linux兼容性问题不大）  \n编辑器：pycharm  \n\n## 💿 安装\n环境依赖`requests`和`nonebot_plugin_htmlrender`库   \n部分功能需要修改`__init__.py`的`header1`的`cookie`，获取自己的cookie，填入才能正常使用！  \n\n### nb-cli安装（推荐）\n在你bot工程的文件夹下，运行cmd（运行路径要对啊），执行nb命令安装插件，插件配置会自动添加至配置文件\n```nb plugin install nonebot_plugin_searchBiliInfo```\n\n### 本地安装\n先安装下 `pip install requests` 和 `pip install nonebot_plugin_htmlrender`  \n将文件夹clone到你的机器人插件下的对应插件目录内（一般为机器人文件夹下的src/plugins），然后把nonebot_plugin_searchBiliInfo文件夹里的内容拷贝至上一级目录即可。  \n也可以直接下载压缩包到插件目录解压，然后同样提取nonebot_plugin_searchBiliInfo至上一级目录。  \n目录结构： ```你的bot/src/plugins/nonebot_plugin_searchBiliInfo/__init__.py```  \n```git clone https://github.com/Ikaros-521/nonebot_plugin_searchBiliInfo.git```  \n\n### pip安装\n```pip install nonebot_plugin_searchBiliInfo```  \n打开 nonebot2 项目的 ```bot.py``` 文件, 在其中写入  \n```nonebot.load_plugin(\'nonebot_plugin_antiinsult\')```  \n当然，如果是默认配置的nonebot2的话，在bot路径```pyproject.toml```的```[tool.nonebot]```的```plugins```中添加```nonebot_plugin_searchBiliInfo```即可\n\n## 🎉 功能\n通过uid 或 设定好的短语 或 b站接口搜索查询指定b站用户的粉丝、舰团信息；直播收益数据；直播观看信息；关键词搜昵称、UID等信息。\n\n## 👉 命令\n\n### /查\n命令结构：```/查 uid+用户uid或昵称关键词```  \n例如：```/查 uid3709626``` 或 ```/查 bishi```  \nbot返回内容：  \n![](docs/search.png)\n\n### /查直播\n命令结构：```/查直播 uid+用户uid或昵称关键词 场次数（默认不写为全部）```  \n例如：```/查直播 uid3709626 1``` 或 ```/查直播 bishi```  \nbot返回内容（图片）：  \n![](docs/live_info.png)\n\n### /查舰团\n命令结构：```/查舰团 uid+用户uid或昵称关键词```  \n例如：```/查舰团 uid3709626``` 或 ```/查舰团 bishi```  \nbot返回内容(图片)：  \n![](docs/guard.png)\n\n### /查昵称\n命令结构：```/查昵称 昵称关键词```  \n例如：```/查昵称 伊卡洛斯```\nbot返回内容(图片)：  \n![](docs/search_name.png)\n\n### /查收益\n命令结构：```/查收益 uid+用户uid或昵称关键词 收益类型(默认1: 礼物，2: 上舰，3: SC) 倒叙第n场(从0开始)```  \n例如：```/查收益 uid3709626 礼物 1``` 或 ```/查收益 bishi 2 0```  \nbot返回内容(图片)：  \n![](docs/income.png)\n\n### /查成分 观看\n命令结构：```/查成分 观看 uid+用户uid或昵称关键词```  \n例如：```/查成分 观看 uid666666``` 或 ```/查成分 观看 bishi```  \nbot返回内容(图片)：  \n![](docs/watch.png)\n\n### /查成分 弹幕\n命令结构：```/查成分 弹幕 uid+用户uid或昵称关键词 查询的主播昵称关键词或uid+ 页数 条数（不填默认3）```  \n例如：```/查成分 弹幕 uid3709626 Love丶伊卡洛斯 1```   \nbot返回内容(图片)：  \n![](docs/danmu.png)\n\n\n## ⚙ 拓展\n启用关键词搜索，需要修改__init__.py的header1的cookie，获取自己的cookie，填入。\n\n命令修改：修改data.py，在文件头部追加你需要定义的用户的json串，注意json格式！！！\n\n返回内容格式修改对应的msg、out_str变量的内容  \n\n## 📝 更新日志\n\n<details>\n<summary>展开/收起</summary>\n\n### 0.0.1\n\n- 插件初次发布\n\n### 0.1.0\n\n- 更新基于vtbs.moe的主播数据，添加关键词搜索功能\n\n### 1.0.0\n\n新增以下功能（其实是LX_Bot的相关命令融进来了）\n- /查 昵称关键词\n- /查直播 昵称关键词 场次数\n- /查舰团 昵称关键词\n- /查昵称 昵称关键词\n- /查直播 收益类型(默认1: 礼物，2: 上舰，3: SC) 用户uid或昵称关键词 倒叙第n场(从0开始)\n- /查成分 观看 昵称关键词\n- /查成分 弹幕 查询的目标人 查询的主播 页数 条数\n\n</details>\n\n## 致谢\n- [nonebot-plugin-htmlrender](https://github.com/kexue-z/nonebot-plugin-htmlrender) - 图片合成的好手\n- [danmaku.suki.club](https://danmaku.suki.club/) - b站主播、用户弹幕直播信息等来源（开放API接口很赞！）\n- [vtbs.moe](https://vtbs.moe) - VTB本地数据信息来源（还有数据提供，TQL）  \n\n## 项目打包上传至pypi\n\n官网：https://pypi.org，注册账号，在系统用户根目录下创建`.pypirc`，配置  \n``` \n[distutils] \nindex-servers=pypi \n \n[pypi] repository = https://upload.pypi.org/legacy/ \nusername = 用户名 \npassword = 密码\n```\n\n### poetry\n\n```\n# 参考 https://www.freesion.com/article/58051228882/\n\n# 1、安装poetry\npip install poetry\n\n# 2、初始化配置文件（根据提示填写）\npoetry init\n\n# 3、微调配置文件pyproject.toml\n\n# 4、运行 poetry install, 可生成 “poetry.lock” 文件（可跳过）\npoetry install\n\n# 5、编译，生成dist\npoetry build\n\n# 6、发布\npoetry publish\n\n```\n\n### twine\n\n```\n# 参考 https://www.cnblogs.com/danhuai/p/14915042.html\n#创建setup.py文件 填写相关信息\n\n# 1、可以先升级打包工具\npip install --upgrade setuptools wheel twine\n\n# 2、打包\npython setup.py sdist bdist_wheel\n\n# 3、可以先检查一下包\ntwine check dist/*\n\n# 4、上传包到pypi（需输入用户名、密码）\ntwine upload dist/*\n```',
    'author': 'Ikaros',
    'author_email': '327209194@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Ikaros-521/nonebot_plugin_searchBiliInfo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
