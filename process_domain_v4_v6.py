#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/12/15 10:54
# @Author: XiangyuTang
# @File  : process_domain_v4_v6.py
import pandas as pd

# df = pd.read_csv('domain_v4v6_info.csv')
# # print(df.duplicated())
# df.drop_duplicates(subset=['domain'],keep='last')
# df.to_csv('domain_v4v6_info_unique1.csv',index=False, encoding='utf_8_sig')

# df1 = pd.read_csv('domain_v4v6_info_unique1.csv')
# # df = df.drop_duplicates(['domain'])
# # df.to_csv('domain_v4v6_info_unique1.csv',index=False, encoding='utf_8_sig')
# print(df1.describe())
#
# df2 = pd.read_csv('top-1m.csv')
# # df = df.drop_duplicates(['domain'])
# # df.to_csv('domain_v4v6_info_unique1.csv',index=False, encoding='utf_8_sig')
# print(df2.describe())




# print(653952/687192)
# print(658573/687192)
# print(652643/687192)
# print(648932/687192)
# print(647635/687192)
# print(648521/687192)
# print(647589/687192)
# print(647942/687192)
# print(646871/687192)
# print(649294/687192)
''' 十周IPv6部署率
option = {
    backgroundColor:'white',
    xAxis: {
        type: 'category',
        boundaryGap: false,
        name:'周次',
        textStyle: {
            fontSize: 18
        },
        data: ['1', '2', '3', '4', '5', '6', '7','8','9','10']
    },
    yAxis: {
        type: 'value',
        min:'0.94',
        name:'域名IPv4 & IPv6部署率'
    },
    series: [{
        data: [0.9516292389899766,
                0.9583537060966949,
                0.9497243856156649,
                0.944324148127452,
                0.942436757121736,
                0.9437260620030501,
                0.9423698180421193,
                0.9428835027183087,
                0.9413249863211446,
                0.9448509295800882
                ],
        type: 'line',
        color:'black',
        areaStyle: {color:'black'}
    }]
};
'''
pd.set_option('display.max_columns', None)
df = pd.read_csv("v4v6_comparison_w1.csv")
print(df.describe())