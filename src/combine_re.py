import glob
import pandas as pd
from rich.progress import Progress


dir_path = 'data\\relations'

# 获取目录中所有 CSV 文件的文件名
csv_files = glob.glob(f"{dir_path}\\*.csv")

# 创建一个空的DataFrame
result = pd.DataFrame(columns=[':START_ID', 'Distance', ':END_ID', ':TYPE'])

with Progress() as progress:
    # 创建任务，并设置总数
    task = progress.add_task("[green]Processing...", total=len(csv_files))

    # 循环遍历CSV文件
    for file in csv_files:
        # 读取CSV文件
        df = pd.read_csv(
            file, usecols=['id1', 'coord1', 'distance', 'id2', 'coord2'])

        # 对数据进行处理，生成新的DataFrame
        new_df = pd.DataFrame({
            ':START_ID': df['id1'],
            'Distance': df['distance'],
            ':END_ID': df['id2'],
            ':TYPE': 'Near by'
        })

        # 将新的DataFrame合并到结果DataFrame中
        result = pd.concat([result, new_df])
        
        # 更新进度条状态
        progress.update(task, advance=1)

# 将结果保存到CSV文件中
result.to_csv('data\\merged_data.csv', index=False)
