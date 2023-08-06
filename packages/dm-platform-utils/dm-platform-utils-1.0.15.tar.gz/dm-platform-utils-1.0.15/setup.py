#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   setup.py
@Time    :   2022/11/10 14:38:09
@Author  :   Shenxian Shi 
@Version :   
@Contact :   shishenxian@bluemoon.com.cn
@Desc    :   None
'''

# here put the import lib
from setuptools import setup, find_packages

setup(
    name='dm-platform-utils',
    version='1.0.15',
    description='Data mining platform develop utils',
    author='Shenxian Shi',
    author_email='shishenxian@bluemoon.com.cn',
    url='http://gitlab.admin.bluemoon.com.cn/DM_group/dm-platform-utils.git',
    packages=['dm_platform_utils'],
    package_dir={'dm_platform_utils': 'src/dm_platform_utils'},
    package_data={'dm_platform_utils': ['conf/*.yml']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'bmai-dm-hbase~=0.1.8',
        'dm-easy-db~=0.1.1',
        'requests==2.28.1'
    ],
    license=open('LICENSE.md').read(),
    long_description=open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown'
)
