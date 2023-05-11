import pandas as pd

"""
# 读取csv文件
df = pd.read_csv("data\\sight.csv")

# 提取City列数据
cities = df["City"]

# 统计城市数量
unique_cities = set(cities)
num_cities = len(unique_cities)

print("共出现了{}种城市".format(num_cities))

# 将城市名保存到txt文件中
with open("data\\cities_sight.csv", "w") as f:
    for city in unique_cities:
        f.write(city + "\n")
"""
# 读取csv文件
df = pd.read_csv("data\\cities.csv")

# 提取City列数据
cities = df["City"]

unique_cities = set(cities)


# 将城市名保存到txt文件中
with open("data\\cities_clean.csv", "w") as f:
    for city in unique_cities:
        f.write(city + "\n")