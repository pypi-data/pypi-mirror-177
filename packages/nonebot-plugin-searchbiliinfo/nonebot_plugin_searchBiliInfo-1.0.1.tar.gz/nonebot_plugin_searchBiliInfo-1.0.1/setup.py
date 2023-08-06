#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="nonebot_plugin_searchBiliInfo",
    version="1.0.1",
    keywords=["pip", "searchBiliInfo", "nonebot"],			# 关键字
    description="A plugin for nonebot2. Query Bilibili user information", 	# 描述
    long_description="A plugin for nonebot2. Query Bilibili user information（一个Nonebot2的插件，b站用户信息查询插件【粉丝、舰团信息；直播收益数据；直播观看信息；关键词搜昵称、UID等】）",
    long_description_content_type="text/x-rst",
    license="MIT Licence",		# 许可证

    # 项目相关文件地址，一般是github项目地址即可
    url="https://github.com/Ikaros-521/nonebot_plugin_searchBiliInfo",
    author="Ikaros-521",			# 作者
    author_email="327209194@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["nonebot2", "nonebot-adapter-onebot", "requests", "nonebot_plugin_htmlrender"]  # 这个项目依赖的第三方库
)
