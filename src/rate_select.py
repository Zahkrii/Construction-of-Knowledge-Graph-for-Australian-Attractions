import pandas as pd


# 读取csv文件
df = pd.read_csv("data\\tmp_merged_place.csv")

# 提取列数据
raw = df["Rate"]

uniques = set(raw)


# 将保存到txt文件中
with open("data\\en_rate.csv", "w") as f:
    for one in uniques:
        f.write(f"{one}\n")