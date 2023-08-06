import os
from setuptools import setup, find_packages


# # 如果readme文件中有中文，那么这里要指定encoding='utf-8'，否则会出现编码错误
# with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as readme:
#       README = readme.read()

# 允许setup.py在任何路径下执行
# os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='HPGCseismic',
    version='0.0.9',
    description='Seismic data processing',
    author='Yanwen Wei',
    author_email='weiyw17@gmail.com',
    requires= ['os','numpy','struct'], # 定义依赖哪些模块
    url="https://github.com/weiyw16/HPGCseismic.git",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8').read(),              # 详细描述（一般会写在README.md中）
    long_description_content_type="text/markdown",  # README.md中描述的语法（一般为markdown）
    packages=find_packages(),  # 系统自动从当前目录开始找包
    # 如果有的文件不用打包，则只能指定需要打包的文件
    #packages=['代码1','代码2','__init__']  #指定目录中需要打包的py文件，注意不要.py后缀
    platforms="any",
    classifiers=[                    # 指定该库依赖的Python版本、license、操作系统之类的
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
    ],
    install_requires=[               # 该库需要的依赖库
            # 'os',
            # 'struct',
        ],
    py_modules=["utils.binIO"]
    )

'''
name : 打包后包的文件名
version : 版本号
author : 作者
author_email : 作者的邮箱
py_modules : 要打包的.py文件
packages: 打包的python文件夹
include_package_data : 项目里会有一些非py文件,比如html和js等,这时候就要靠include_package_data 和 package_data 来指定了。
                        package_data:一般写成{‘your_package_name’: [“files”]}, 
                        include_package_data还没完, 还需要修改MANIFEST.in文件.MANIFEST.in文件的语法为: 
                        include xxx/xxx/xxx/.ini/(所有以.ini结尾的文件,也可以直接指定文件名)
license : 支持的开源协议
description : 对项目简短的一个形容
ext_modules : 是一个包含Extension实例的列表,Extension的定义也有一些参数。
ext_package : 定义extension的相对路径
requires : 定义依赖哪些模块
provides : 定义可以为哪些模块提供依赖
data_files :指定其他的一些文件(如配置文件),规定了哪些文件被安装到哪些目录中。如果目录名是相对路径,则是相对于sys.prefix或sys.exec_prefix的路径。如果没有提供模板,会被添加到MANIFEST文件中。
'''
