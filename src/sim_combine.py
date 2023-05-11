import pandas as pd
from utils.textsim import getSimCustomModel


def sim(txt1, txt2):
    return getSimCustomModel(txt1, txt2) > 0.85


df1 = pd.read_csv("data\\ctrip.csv")
df2 = pd.read_csv("data\\ta.csv")

savepath="data\\merged.csv"

# 遍历两个DataFrame，判断name是否相同，并去除重复数据
merged = []
for i, row1 in df1.iterrows():
    # 遍历data1.csv文件中的每一行，查找在data2.csv中是否存在相同的记录
    is_duplicate = False
    for j, row2 in df2.iterrows():
        if sim(row1["en_name"], row2["name"]):
            # 如果name相似度大于0.85，则认为是重复数据，跳出循环
            is_duplicate = True
            break
    if not is_duplicate:
        # 如果不是重复数据，则将该记录加入到merged列表中
        merged.append(row1)

# 将data2.csv中不重复的记录加入到merged列表中
for i, row2 in df2.iterrows():
    is_duplicate = False
    for j, row1 in df1.iterrows():
        if sim(row1["en_name"], row2["name"]):
            is_duplicate = True
            break
    if not is_duplicate:
        merged.append(row2)

# 将merged列表转换为DataFrame对象并保存到merged.csv文件中
merged_df = pd.DataFrame(merged)
merged_df.to_csv(savepath, index=False)
