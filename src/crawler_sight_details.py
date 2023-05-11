import utils.csv_util as csvUtils
import utils.html as htmlUtils
from utils.translator import translate_by_azure

path = r'ctrip\\sights\\_index.csv'

newpath = r'ctrip\\sights\\sights.csv'


reader, reader_file, count = csvUtils.readCSV(path)

i = 0
for row in reader:
    writer, file = csvUtils.writeCSV(
        newpath, ['c_name', 'e_name', 'address','time', 'tel', 'review', 'intro', 'tickets'])

    isCh = True
    hasSub = True

    html = htmlUtils.getHTML(row['url'])

    # 主标题
    # /html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[1]/div[1]/h1/text()
    main = html.xpath(
        '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[1]/div[1]/h1/text()')
    main = main[0]
    if (main.encode('UTF-8').isalpha()):
        isCh = False
    print(f'{i+1}/{count}::{main}')
    # 副标题
    # /html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/h2/text()
    try:
        sub = html.xpath(
            '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/h2/text()')
        sub = sub[0]
    except:
        # print('无副标题')
        hasSub = False
        sub = ''
    # 中英文翻译
    c_name = ''
    e_name = ''
    if (not (isCh) and not (hasSub)):
        c_name = translate_by_azure(main)
        e_name = main
    else:
        c_name = main
        e_name = sub
    # 地址
    # /html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[3]/div[1]/p[2]/text()
    try:
        address = html.xpath(
            '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[3]/div[1]/p[2]/text()')
        address = address[0]
    except:
        address = ''
    # 电话与开放时间
    try:
        test = html.xpath(
            '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[3]/div[2]/p[1]/text()')
        if (test[0] == '开放时间'):
            time = html.xpath(
                '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[3]/div[2]/p[2]/text()')
            time = time[0]
            tel = html.xpath(
                '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[3]/div[3]/p[2]/text()')
            tel = tel[0]
        else:
            tel = html.xpath(
                '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[3]/div[2]/p[2]/text()')
            tel = tel[0]
            time=''
    except:
        time = ''
        tel = ''
    # 评分
    # /html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[2]/div/p[1]/text()
    try:
        review = html.xpath(
            '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[2]/div/p[1]/text()')
        review = review[0]
    except:
        review = ''
    # 简介
    # /html/body/div[2]/div[2]/div/div[3]/div/div[4]/div[1]/div[2]/div/div[2]/div/div/p[1]/text()
    try:
        intro = html.xpath(
            '/html/body/div[2]/div[2]/div/div[3]/div/div[4]/div[1]/div[2]/div/div[2]/div/div/p[1]/text()')
        intro = intro[0]
    except:
        intro = ''
    # 门票
    # /html/body/div[2]/div[2]/div/div[3]/div/div[4]/div[1]/div[2]/div/div[4]/div/text()
    try:
        tickets = html.xpath(
            '/html/body/div[2]/div[2]/div/div[3]/div/div[4]/div[1]/div[2]/div/div[4]/div/text()')
        tickets = ''.join(tickets)
    except:
        tickets = ''

    writer.writerow({'c_name': c_name, 'e_name': e_name, 'address': address,'time':time,
                    'tel': tel, 'review': review, 'intro': intro, 'tickets': tickets})

    i += 1
    # if (i > 0):break
    csvUtils.closeCSV(file)
csvUtils.closeCSV(reader_file)
