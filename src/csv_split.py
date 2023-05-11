import pandas as pd

# 读取csv文件
df = pd.read_csv("data\\newnode.csv")

# 获取文件总行数
row_num = len(df)

# 确定每个小文件要包含的数据量
step = 100000

for start in range(0, row_num, step):
    stop = start + step
    filename = "data\\node\\newnode_{}-{}.csv".format(start, stop)
    d = df[start: stop]
    print("Saving file : " + filename + ", data size : " + str(len(d)))
    d.to_csv(filename, index=None)
