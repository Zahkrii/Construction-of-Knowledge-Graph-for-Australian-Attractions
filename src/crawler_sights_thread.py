import threading
import utils.csv_util as csvUtils
import utils.html as htmlUtils
from tqdm import tqdm


class CrawlThread(threading.Thread):
    def __init__(self, name, link_range):
        threading.Thread.__init__(self)
        self.name = name
        self.link_range = link_range

    def run(self):
        print("Starting " + self.name)
        crawl(self.name, self.link_range)
        print("Exiting " + self.name)


def crawl(name, link_range):
    for j in range(link_range[0], link_range[1]+1):
        # 读取城市名及 URL
        reader, city_file, count = csvUtils.readCSV(
            f'ctrip/citys/citys{j:0>2d}.csv')
        print(f'{name}：开始处理：citys{j:0>2d}.csv')
        i = 0
        # 循环处理每个城市
        for row in reader:

            tmplist = row['url'].split('/')
            tmplist = tmplist[4].split('.')

            try:
                html = htmlUtils.getHTMLbyProxy(
                    f'https://you.ctrip.com/sight/{tmplist[0]}.html')
            except:
                html = htmlUtils.getHTML(
                    f'https://you.ctrip.com/sight/{tmplist[0]}.html')

            sightSum = html.xpath(
                '/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[3]/div[12]/div/span/b/text()')
            if (sightSum == []):
                sightSum = html.xpath(
                    '/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[3]/div[11]/div/span/b/text()')

            print(f' - {name}：第{i+1}行：' + row['city'] + f'：共{sightSum[0]}页')

            # 创建存储景点名称及url的index文件 citys00.000.悉尼.csv
            # citys00 表示来自 citys00.csv，000 表示是 citys00.csv 的第几个城市

            sight_filepath = csvUtils.createCSV(
                f'ctrip/sights/index/citys{j:0>2d}.{i:0>3d}.' + row['city'] + '.csv', ('sight', 'url'))
            writer, sight_file = csvUtils.writeCSV(
                sight_filepath, ['sight', 'url'])
            maxPage = int(sightSum[0]) + 1
            for per_page in tqdm(range(1, maxPage)):
                try:
                    html = htmlUtils.getHTMLbyProxy(
                        f'https://you.ctrip.com/sight/{tmplist[0]}/s0-p{per_page}.html')
                except:
                    html = htmlUtils.getHTML(
                        f'https://you.ctrip.com/sight/{tmplist[0]}/s0-p{per_page}.html')
                try:
                    for p in range(1, 6):
                        name = html.xpath(
                            '/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[3]/div[' + str(p) + ']/div[2]/dl/dt/a[1]/text()')
                        link = html.xpath(
                            '/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[3]/div[' + str(p) + ']/div[2]/dl/dt/a[1]/@href')
                        # 写入一行
                        writer.writerow(
                            {'sight': name[0], 'url': 'https://you.ctrip.com' + link[0]})

                    for p in range(7, 12):
                        name = html.xpath(
                            '/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[3]/div[' + str(p) + ']/div[2]/dl/dt/a[1]/text()')
                        link = html.xpath(
                            '/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[3]/div[' + str(p) + ']/div[2]/dl/dt/a[1]/@href')
                        # 写入一行
                        writer.writerow(
                            {'sight': name[0], 'url': 'https://you.ctrip.com' + link[0]})
                except:
                    print(f' - {name}：第{i+1}行：' +
                          row['city'] + f'：第{per_page}页元素不足10个，可能是末页')
            csvUtils.closeCSV(sight_file)
            print(f' - {name}：第{i+1}行：' + row['city'] + '：处理完毕')
            # 一个城市处理完毕
            i = i + 1
        # For循环结尾
        csvUtils.closeCSV(city_file)


threads = []
link_range_list = [(3, 6), (6, 9), (9, 12), (12, 15), (15, 18),
                   (18, 21), (21, 24), (24, 27), (27, 30), (30, 33), (33, 36)]


for i in range(1, 11):
    # 创建4个新线程
    thread = CrawlThread("thread_" + str(i), link_range=link_range_list[i-1])
    # 开启新线程
    thread.start()
    # 添加新线程到线程列表
    threads.append(thread)

# 等待所有线程完成
for thread in threads:
    thread.join()

print("Exiting Main Thread...")
