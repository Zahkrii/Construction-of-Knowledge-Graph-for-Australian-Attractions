import pandas as pd

# 读取第一张表格
table1 = pd.read_csv('data\\tmp_merged_place.csv')

# 读取第二张表格
table2 = pd.read_csv('data\\cities.csv')

# 根据City列合并两张表格
merged_table = pd.merge(table1, table2, on='City', how='inner')[['ID:ID', 'City_ID:ID']]

# 保存为新的CSV文件
merged_table.to_csv('new_table.csv', index=False)