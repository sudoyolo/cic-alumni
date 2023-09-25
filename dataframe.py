import numpy as np
import pandas as pd

merged_list = []
df1 = pd.DataFrame()

sheet_name = ['2011-2015', '2012-2016','2013-2017', '2014-2018', '2015-2019', '2016-2020', '2017-2021', '2018-2022', '2019-2023']

for i in range(len(sheet_name)):

 
 merged_list.append(pd.read_excel('FinalSheet.xlsx', sheet_name[i]))

df1 = pd.concat(merged_list, ignore_index=True)

df1.to_csv('MergedList.csv')