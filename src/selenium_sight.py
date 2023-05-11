from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import utils.csv_util as csvUtils
from tenacity import retry, wait_fixed, stop_after_attempt
from utils.translator import translate_by_azure
from utils.lang_detect import judge_language

service = Service(executable_path='driver\msedgedriver.exe')
options = webdriver.EdgeOptions()
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('log-level=3')
browser = webdriver.Edge(service=service, options=options)

path = r'ctrip\\sights\\_index.csv'
newpath = r'ctrip\\sights\\sights.csv'
reader, reader_file, count = csvUtils.readCSV(path)


field = ['c_name', 'e_name', 'city', 'address',
         'time', 'tel', 'rate', 'intro', 'tickets', 'url']


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2), reraise=True)
def try_get_title():
    element = browser.find_element(
        By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[1]/div[1]/h1')
    return element


i = 1
for row in reader:
    # 获取城市
    link_list = row['url'].split("/")
    temp = link_list[4]
    temp_list = re.split("\d+", temp)
    city = temp_list[0]
    # 打开文件
    writer, file = csvUtils.writeCSV(newpath, field)
    # 打开链接
    browser.get(row['url'])

    # 名称
    title = try_get_title()
    title = title.text

    # 副标题
    try:
        sub = browser.find_element(
            By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/h2')
        sub = sub.text
    except:
        sub = ''

    # 中英文翻译
    if ((sub == '') and (judge_language(title) == 'en')):
        c_name = translate_by_azure(title)
        e_name = title
    else:
        c_name = title
        e_name = sub

    print(f'第{i}项::{c_name}::{e_name}')

    # 电话与开放时间
    try:
        test = browser.find_element(
            By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[3]/div[2]/p[1]')
        if (test.text == '开放时间'):
            time = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[3]/div[2]/p[2]')
            time = time.text
            tel = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[3]/div[3]/p[2]')
            tel = tel.text
        else:
            tel = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[3]/div[2]/p[2]')
            tel = tel.text
            time = ''
    except:
        time = ''
        tel = ''

    # 地址
    try:
        address = browser.find_element(
            By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[3]/div[1]/p[2]')
        address = address.text
    except:
        address = ''

    # 简介
    try:
        intro = browser.find_element(
            By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/div/div[4]/div[1]/div[1]/div/div[2]/div/div/p')
        intro = intro.text
    except:
        try:
            intro = browser.find_element(
            By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/div/div[4]/div[1]/div[2]/div/div[2]/div/div/p[1]')
            intro = intro.text
        except:
            intro = ''

    # 评分
    try:
        rate = browser.find_element(
            By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[2]/div/p[1]')
        rate = rate.text
    except:
        rate = ''

    # 门票
    try:
        tickets = browser.find_element(
            By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/div/div[4]/div[1]/div[2]/div/div[4]/div')
        tickets = tickets.text
    except:
        tickets = ''

    writer.writerow({'c_name': c_name, 'e_name': e_name, 'city': city, 'address': address, 'time': time,
                    'tel': tel, 'rate': rate, 'intro': intro, 'tickets': tickets, 'url': row['url']})
    csvUtils.closeCSV(file)
    i += 1
# 退出
browser.quit()
