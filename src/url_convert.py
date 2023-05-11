import csv
import utils.csv_util as csvUtils

index = 4

reader, city_file, count = csvUtils.readCSV(
    f'ctrip/citys/citys{index:0>2d}.csv')

file = open(f'ctrip/citys/o/citys{index:0>2d}s.csv',
            'a+', newline='', encoding='utf-8-sig')
writer = csv.DictWriter(file, ['col1'])

print(f'开始处理：citys{index:0>2d}.csv')

for row in reader:

    tmplist = row['url'].split('/')
    tmplist = tmplist[4].split('.')

    url = f'https://you.ctrip.com/sight/{tmplist[0]}.html'
    writer.writerow({'col1': url})

print(f'处理完成：citys{index:0>2d}.csv')
file.close()
