#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   test_hbase_client.py.py
@Time    :   2022/5/5 10:29
@Author  :   Shenxian Shi 
@Version :   
@Contact :   shishenxian@bluemoon.com.cn
@Desc    :   None
"""

# here put the import lib
import sys
sys.path.append('..')

from bmai_dm_hbase.hbase_client import HBaseClient


def test_server_type1():
    hosts = '192.168.39.3'
    ports = 9090
    HBaseClient(host=hosts, port=ports, env='test')


def test_server_type2():
    hosts = '192.168.39.3'
    ports = 9090
    HBaseClient(host=hosts, port=ports, file_path='../conf/hbase.yml', server_type='abcd', env='test')


def test_server_type3():
    hosts = '192.168.39.3'
    ports = 9090
    HBaseClient(host=hosts, port=ports, file_path='../conf/hbase1.yml', server_type='prd', env='prd')
