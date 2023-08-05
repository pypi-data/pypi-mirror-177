#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_insert.py
@Time    :   2022/10/09 17:27:53
@Author  :   Shenxian Shi 
@Version :   
@Contact :   shishenxian@bluemoon.com.cn
@Desc    :   None
'''

# here put the import lib
import sys
import os

sys.path.append('..')
sys.path.append(os.getcwd())
from bmai_dm_hbase.hbase_client import HBaseClient


if __name__ == '__main__':
    hbase = HBaseClient('192.168.235.51', 9090)
    hbase.build_pool()
    datas = hbase.scan_tables('pred_system:fact_pred_gyxt_shop_result')
    data = datas[1]
    print(data[0])
    hbase.create_tbl('pred_system:dm_hbase_test', table_desc={'0': dict()})
    hbase.insert(table_name='pred_system:dm_hbase_test', datas=dict(data))
    data = hbase.scan_tables('pred_system:dm_hbase_test')[1]
    print(data[0])
    hbase.delete_tbl('pred_system:dm_hbase_test')