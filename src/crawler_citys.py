import requests
from lxml import etree
import csv

# 定义UA，伪装爬虫，取了Edge浏览器的UA
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.0.0'
}

for k in range(0, 36):
    # 打开 csv
    csvfile = open(f'ctrip/citys/citys{k:0>2d}.csv',
                   'a+', newline='', encoding='utf-8-sig')
    print(f'创建：ctrip/citys/citys{k:0>2d}.csv')
    writer = csv.wwwriter(csvfile)
    header = ('city', 'url')
    writer.writerow(header)
    # 保存
    csvfile.close()

    for j in range(1+10*k, 11+10*k):
        # 从携程 Get 请求静态文本内容
        res = requests.get(
            url='https://you.ctrip.com/countrysightlist/australia100048/p' + str(j) + '.html', headers=headers)
        # print(res.text)

        # 将文本转换成HTML文档
        html = etree.HTML(res.text)

        # XPath：
        # 悉尼: /html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[1]/dl/dt/a/text()
        # 悉尼: /html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[1]/dl/dt/a
        # 墨尔本: /html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[2]/dl/dt/a/text()
        # 布里斯班: /html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[3]/dl/dt/a/text()
        # ...
        # 菲利普岛: /html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[10]/dl/dt/a/text()
        # 可看出div顺序从1到10，循环获取

        csvfile = open(
            f'ctrip/citys/citys{k:0>2d}.csv', 'a+', newline='', encoding='utf-8-sig')
        fieldnames = ['city', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 通过XPath定位城市名，每页10个城市
        for i in range(1, 11):
            name = html.xpath(
                '/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[' + str(i) + ']/dl/dt/a/text()')
            link = html.xpath(
                '/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[' + str(i) + ']/dl/dt/a/@href')
            # print(name[0]+': https://you.ctrip.com'+link[0])
            # 写入一行

            writer.writerow(
                {'city': name[0], 'url': 'https://you.ctrip.com' + link[0]})
        
        csvfile.close()
    print(f'完成：ctrip/citys/citys{k:0>2d}.csv')
    # 位于第二页的史蒂芬斯湾XPath: /html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[1]/dl/dt/a/text()
    # 与第一页无异，由此可通过循环获取每页的内容

# 打开 csv
csvfile = open(f'ctrip/citys/citys36.csv','a+', newline='', encoding='utf-8-sig')
print(f'创建：ctrip/citys/citys36.csv')
# 构建字段名称，也就是key
fieldnames = ['city', 'url']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# 保存
csvfile.close()

for j in range(361, 365):
    # 从携程 Get 请求静态文本内容
    res = requests.get(
        url='https://you.ctrip.com/countrysightlist/australia100048/p' + str(j) + '.html', headers=headers)
    # print(res.text)

    # 将文本转换成HTML文档
    html = etree.HTML(res.text)

    # XPath：
    # 悉尼: /html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[1]/dl/dt/a/text()
    # 悉尼: /html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[1]/dl/dt/a
    # 墨尔本: /html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[2]/dl/dt/a/text()
    # 布里斯班: /html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[3]/dl/dt/a/text()
    # ...
    # 菲利普岛: /html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[10]/dl/dt/a/text()
    # 可看出div顺序从1到10，循环获取

    csvfile = open(f'ctrip/citys/citys36.csv', 'a+', newline='', encoding='utf-8-sig')
    fieldnames = ['city', 'url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 通过XPath定位城市名，每页10个城市
    for i in range(1, 11):
        name = html.xpath('/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[' + str(i) + ']/dl/dt/a/text()')
        link = html.xpath('/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div[' + str(i) + ']/dl/dt/a/@href')
        # print(name[0]+': https://you.ctrip.com'+link[0])
        # 写入一行

        writer.writerow({'city': name[0], 'url': 'https://you.ctrip.com' + link[0]})
        
    csvfile.close()
print(f'完成：ctrip/citys/citys36.csv')