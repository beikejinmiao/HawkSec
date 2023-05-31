#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pandas as pd


data = [{'name': 'ljm', 'idcard': '500228199108262851'}, {'name': 'jx', 'idcard': '500228199111052249'}]
df = pd.DataFrame(data)
df['idcard'] = df['idcard'].astype(str)
print(df.dtypes)
df.to_csv('idcard_csv_test.csv')
