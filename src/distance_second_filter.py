import time
import pandas as pd
from utils.str_util import check_str

path = 'data\\merged_data.csv'
field=[':START_ID','Distance',':END_ID',':TYPE']

newpath='data\\distance.csv'


# 选定要筛选的列名和阈值
column_name = 'Distance'
threshold = 3

# 读取CSV文件
df = pd.read_csv(path)

# 使用布尔索引筛选出满足条件的数据
filtered_data = df[df[column_name] <= threshold]

filtered_data=filtered_data[filtered_data[':START_ID'].str.contains('sight')]
    
# 打印筛选后的数据
time_str = time.strftime('%H:%M:%S', time.localtime(time.time()))
print(f"[{time_str}] 筛选出的数据:")
print(filtered_data, "\n")
    
# 保存数据
time_str = time.strftime('%H:%M:%S', time.localtime(time.time()))
print(f"[{time_str}] 保存至 {newpath}")
filtered_data.to_csv(newpath, index=None)