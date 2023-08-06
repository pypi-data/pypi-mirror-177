#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_DataWriter.py
@Time    :   2022/11/04 10:34:22
@Author  :   Shenxian Shi 
@Version :   
@Contact :   shishenxian@bluemoon.com.cn
@Desc    :   None
'''

# here put the import lib
import os
import sys
import json
from copy import deepcopy
sys.path.append('..')
sys.path.append('../src')
sys.path.append(os.getcwd())
print(os.getcwd())

import pandas as pd

from src.dm_platform_utils.DataWriter import DataWriter

YOUR_ACCOUNT = ''
YOUR_PASSWD = ''
YOUR_TEST_HOST = ''
YOUR_PRD_HOST = ''
info = {
    'token_param':
        {
            'account': YOUR_ACCOUNT,
            'pwd': YOUR_PASSWD
        },
    'model_name': 'testing1',
    'model_version': 'v1.0.1',
    'hbase':
        {
            'test': {
                'host': YOUR_TEST_HOST,
                'port': 9090,
                'table_name': 'pred_system:fact_alg_dm_pred_detail',
                'rowkeys_col': 'model_cd', 
                'family': 'INFO'
            },
            'prd': {
                'host': YOUR_PRD_HOST,
                'port': 9090,
                'table_name': 'pred_system:fact_alg_dm_pred_detail',
                'rowkeys_col': 'model_cd', 
                'family': 'INFO'
            }
        },
    'env': 'test'
}

data = pd.DataFrame({
    'model_date': ['202209', '202209'],
    'data_date': ['202210', '202211'],
    'date_type': ['3', '3'],
    'first_dim': ['1', '1'],
    'second_dim': ['14', '14'],
    'third_dim': ['tmall', 'tmall'],
    'fourth_dim': ['102', '102'],
    'fifth_dim': ['10001244', '10001244'],
    'date_diff': ['1', '2'],
    'create_time': ['2022-11-04 11:45:00', '2022-11-04 11:45:00'],
    'pred_pay_amt': ['1223123.1231', '31231231.323'],
    'pred_pay_cnt': ['231231', '3324234']
})

writer = DataWriter(info=info)


class TestClass:
    def test_get_model_data(self):
        writer._get_model_data()
        assert len(writer._model_data) > 0
        
    def test_get_dim_data(self):
        writer._get_dim_data()
        assert len(writer._dim_data) > 0

    def test_insert_model_data(self):
        writer.insert_model_data(
            {
                'dateType': 3,
                'deployStatus': 1,
                'dimLevel': 5,
                'lastEndTime': '2022-11-04 12:15:00',
                'lastRunTime': 1800,
                'lastStartTime': '2022-11-04 11:45:00',
                'modelDesc': 'testing12345',
                'modelName': info['model_name'],
                'modelParam': json.dumps({"changepoint_prior_scale": 0.1, "seasonality_prior_scale": 1.0}),
                'modelVersion': info['model_version'],
                'modelStatus': 2
            }
        )
        writer._get_model_data()
        assert len(writer._model_data[writer._model_data['modelDesc'] == 'testing12345'])
        
    def test_update_model_data(self):
        writer.update_model_data(
            {
                'modelDesc': 'Hello, world!'
            }
        )
        writer._get_model_data()
        assert len(writer._model_data[writer._model_data['modelDesc'] == 'Hello, world!'])
        
    def test_insert_dim_data1(self):
        writer.insert_dim_data(
            {
                'dmId': 'tmall_moonmall',
                'dmLevel': 3,
                'dmName': '你好',
                'dmParentId': '33'
            }
        )
        writer._get_dim_data()
        test_level, test_name = writer._dim_data.loc[
            (writer._dim_data['dmId'] == 'tmall_moonmall') &
            (writer._dim_data['dmParentId'] == '33'),
            ['dmLevel', 'dmName']
        ].values[0]
        assert test_level == 3
        assert test_name == '你好'
        
    def test_update_dim_data1(self):
        writer.update_dim_data(
            {
                'dmId': 'tmall_moonmall',
                'dmLevel': 3,
                'dmName': '修改',
                'dmParentId': '33'
            }
        )
        writer._get_dim_data()
        test_level, test_name = writer._dim_data.loc[
            (writer._dim_data['dmId'] == 'tmall_moonmall') &
            (writer._dim_data['dmParentId'] == '33'),
            ['dmLevel', 'dmName']
        ].values[0]
        assert test_level == 3
        assert test_name == '修改'
    
    def test_insert_dim_data2(self):
        writer.insert_dim_data(
            {
                'dmId': '134',
                'dmLevel': 4,
                'dmName': '你好',
                'dmParentId': 'tmall_moonmall'
            }
        )
        writer._get_dim_data()
        test_level, test_name = writer._dim_data.loc[
            (writer._dim_data['dmId'] == '134') &
            (writer._dim_data['dmParentId'] == 'tmall_moonmall'),
            ['dmLevel', 'dmName']
        ].values[0]
        assert test_level == 4
        assert test_name == '你好'
    
    def test_update_dim_data2(self):
        writer.update_dim_data(
            {
                'dmId': '134',
                'dmLevel': 4,
                'dmName': '修改',
                'dmParentId': 'tmall_moonmall'
            }
        )
        writer._get_dim_data()
        test_level, test_name = writer._dim_data.loc[
            (writer._dim_data['dmId'] == '134') &
            (writer._dim_data['dmParentId'] == 'tmall_moonmall'),
            ['dmLevel', 'dmName']
        ].values[0]
        assert test_level == 4
        assert test_name == '修改'
    
    def test_trans_hbase(self):
        from easy_db.db import encrypt_df
        new_writer = DataWriter(info)
        test_data1 = deepcopy(data)
        new_writer._trans_hbase(data=test_data1, rowkeys_col='model_cd', family='INFO')
        test_data = deepcopy(data)
        test_data['parent_model_cd'] = new_writer.parent_md5_id
        test_data = encrypt_df(
            test_data, 
            [
            'parent_model_cd', 'model_date', 'data_date', 
            'date_type', 'first_dim', 'second_dim', 
            'third_dim', 'fourth_dim', 'fifth_dim'
            ]
        )
        model_cd = set(test_data1['model_cd'].values.tolist())
        test_model_cd = set(test_data['uuid'].values.tolist())
        
        col_list = test_data.columns.tolist()
        col_list.remove('uuid')
        test_col = {f'INFO:{c}' for c in col_list}
        cols = test_data1.columns.tolist()
        cols.remove('model_cd')
        cols = set(cols)
        assert model_cd == test_model_cd
        assert test_col == cols
    
    def test_insert_forecast(self):
        from bmai_dm_hbase.hbase_client import HBaseClient
        writer.insert_forecast(
            data=data
        )
        test_hbase = HBaseClient(
            host=info['hbase']['test']['host'],
            port=info['hbase']['test']['port']
        )
        test_hbase.build_pool()
        _, test_data = test_hbase.scan_tables(
            table_name='pred_system:fact_alg_dm_pred_detail'
        )
        test_data1 = deepcopy(data)
        writer._trans_hbase(
            data=test_data1, 
            rowkeys_col=info['hbase']['test']['rowkeys_col'],
            family=info['hbase']['test']['family']
        )
        test_data = dict(test_data)
        model_cd = [f'{c}'.encode() for c in test_data1['model_cd'].values]
        for code in model_cd:
            assert code in test_data.keys()
            continue
