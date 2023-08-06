# Always prefer setuptools over distutils
# To use a consistent encoding
from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))


# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='twitter_crawler',
    version='1.6',
    author='潘闯界',
    author_email='is_chuangjie@163.com',
    description='An Twitter scraping tool without account',
    long_description='An Twitter scraping tool without account',  # 这里是文档内容, 读取readme文件
    long_description_content_type='text/markdown',  # 文档格式
    packages=find_packages(),
    classifiers=[  # 这里我们指定证书, python版本和系统类型
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 这里指定python版本号必须大于3.6才可以安装
    install_requires=['requests']  # 我们的模块所用到的依赖, 这里指定的话, 用户安装你的模块时, 会自动安装这些依赖
)
