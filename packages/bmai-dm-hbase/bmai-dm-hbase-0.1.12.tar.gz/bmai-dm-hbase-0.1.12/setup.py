from email import header


#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   setup.py
@Time    :   2022/02/17 11:18:18
@Author  :   Shenxian Shi 
@Version :   
@Contact :   shishenxian@bluemoon.com.cn
@Desc    :   None
'''

# here put the import lib
from setuptools import setup, find_packages

setup(
    name='bmai-dm-hbase',
    version='0.1.12',
    description='Data mining Group hbase utils',
    author='Shuxin Liang',
    author_email='liangshuxin1@bluemoon.com.cn',
    url='http://gitlab.admin.bluemoon.com.cn/BigData-DataAlgorithm/dm-hbase.git',
    packages=find_packages(),
    # package_dir={'bmai_dm_hbase': '.'},
    install_requires=[
        'ruamel.yaml~=0.15.0',
        'thrift~=0.15.0',
        'thrift-sasl~=0.4.2', 
        'thriftpy~=0.3.9',
        'thriftpy2~=0.4.14',
        'happybase~=1.2.0', 
        'pandas~=1.3.4'
    ],
    python_requires='>=3.6',
    license=open('LICENSE.md').read(),
    long_description=open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown'
)
