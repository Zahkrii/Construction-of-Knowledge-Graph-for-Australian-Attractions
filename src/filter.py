import time
import pandas as pd
import os

path = 'data\\node'
field=['id1','coord1','distance','id2','coord2']

newpath='data\\relations'

# 获取当前目录下的所有CSV文件
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

# 选定要筛选的列名和阈值
column_name = 'distance'
threshold = 5

# 遍历所有CSV文件
for csv_file in csv_files:
    # 读取CSV文件
    df = pd.read_csv(f'{path}\\{csv_file}')

    # 使用布尔索引筛选出满足条件的数据
    filtered_data = df[df[column_name] <= threshold]
    
    # 打印筛选后的数据
    time_str = time.strftime('%H:%M:%S', time.localtime(time.time()))
    print(f"[{time_str}] 从 {csv_file} 筛选出的数据:")
    print(filtered_data, "\n")
    
    # 保存数据
    time_str = time.strftime('%H:%M:%S', time.localtime(time.time()))
    print(f"[{time_str}] 保存至 {newpath}\\{csv_file}\n")
    filtered_data.to_csv(f'{newpath}\\{csv_file}', index=None)