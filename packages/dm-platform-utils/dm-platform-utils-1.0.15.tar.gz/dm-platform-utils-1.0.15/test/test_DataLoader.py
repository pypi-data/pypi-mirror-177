#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_DataLoader.py
@Time    :   2022/11/03 11:43:13
@Author  :   Shenxian Shi 
@Version :   
@Contact :   shishenxian@bluemoon.com.cn
@Desc    :   None
'''

# here put the import lib
import os
import sys
sys.path.append('..')
sys.path.append('../src')
sys.path.append(os.getcwd())
print(os.getcwd())

import numpy as np

from src.dm_platform_utils.DataLoader import DataLoader


YOUR_IMPALA_IP = ''

test1 = DataLoader(
        engine='impala',
        project='gyxt',
        host='192.168.235.53',
        port=21050
    )


class TestClass:
    
    def test_fifth_dim(self):
        fifth_dim_month = test1.get_data(
            dim='fifth_dim', date_type='month'
        )
        assert len(fifth_dim_month) > 0
        assert len(fifth_dim_month.columns.tolist()) == 8
        assert isinstance(
            fifth_dim_month['data_date'].dtypes,
            type(np.dtype('object'))
        )
        assert isinstance(
            fifth_dim_month['first_dim'].dtypes,
            type(np.dtype('object'))
        )
        assert isinstance(
            fifth_dim_month['second_dim'].dtypes,
            type(np.dtype('object'))
        )
        assert isinstance(
            fifth_dim_month['third_dim'].dtypes,
            type(np.dtype('object'))
        )
        assert isinstance(
            fifth_dim_month['fourth_dim'].dtypes,
            type(np.dtype('object'))
        )
        assert isinstance(
            fifth_dim_month['fifth_dim'].dtypes,
            type(np.dtype('object'))
        )
        assert isinstance(
            fifth_dim_month['pay_cnt'].dtypes,
            type(np.dtype(int))
        )
        assert isinstance(
            fifth_dim_month['pay_amt'].dtypes,
            type(np.dtype(float))
        )
    
    def test_second_dim(self):
        second_dim_month = test1.get_data(
            dim='second_dim', date_type='month'
        )
        assert len(second_dim_month) > 0
        assert len(second_dim_month.columns.tolist()) == 5
        
    def test_third_dim(self):
        third_dim_month = test1.get_data(
            dim='third_dim'
        )
        assert len(third_dim_month) > 0
        assert len(third_dim_month.columns.tolist()) == 6
