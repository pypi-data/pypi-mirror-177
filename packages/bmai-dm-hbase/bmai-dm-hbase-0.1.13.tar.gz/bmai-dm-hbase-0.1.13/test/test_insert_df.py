#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_insert_df.py
@Time    :   2022/10/09 17:28:13
@Author  :   Shenxian Shi 
@Version :   
@Contact :   shishenxian@bluemoon.com.cn
@Desc    :   None
'''

# here put the import lib
import sys
import os
import pandas as pd

sys.path.append('..')
sys.path.append(os.getcwd())
from bmai_dm_hbase.hbase_client import HBaseClient


if __name__ == '__main__':
    hbase = HBaseClient('192.168.235.51', 9090)
    hbase.build_pool()
    data = pd.DataFrame(
        {'uuid': ['123', '234', '345'],
         '0:a': ['fewf', 'fwefwe', 'werwer'],
         '0:b': ['gerg', '345324', 'erwe']}
    )
    print(data)
    hbase.create_tbl('pred_system:dm_hbase_test', table_desc={'0': dict()})
    hbase.insert_df(table_name='pred_system:dm_hbase_test', df=data, rowkeys_col='uuid')
    data = hbase.scan_tables('pred_system:dm_hbase_test')[1]
    print(data[0])
    hbase.delete_tbl('pred_system:dm_hbase_test')