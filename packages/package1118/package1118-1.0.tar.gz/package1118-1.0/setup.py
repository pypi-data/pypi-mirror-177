# encoding=utf-8
from distutils.core import setup,Extension

# 打包软件脚本文件必须采用 setup 名称
# 打包函数
setup(
    name='package1118',  # 安装包名
    version='1.0',  # 打包安装软件的版本号
    description="输出方阵",
    long_description="输出方阵",
    author= '207',
    author_email= '321078180@qq.com',
    # url="",  # 包相关网站主页的的访问地址
    # download_url="",  # 下载安装包(zip , exe)的url
    # keywords="math",
    py_modules=['package1118'],  # 设置打包模块，可以多个
    # 对于C,C++,Java 等第三方扩展模块一起打包时，需要指定扩展名、扩展源码、以及任何编译/链接 要求（包括目录、链接库等）
    ext_modules = [Extension('data',['data.c'])],
)