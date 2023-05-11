from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import utils.csv_util as csvUtils
from tenacity import retry, wait_fixed, stop_after_attempt

service = Service(executable_path='driver\msedgedriver.exe')

options = webdriver.EdgeOptions()
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('log-level=3')

browser = webdriver.Edge(service=service, options=options)

browser.get('https://you.ctrip.com/shoppinglist/phillipisland16477.html')

path = r'ctrip\\shops\\shop.csv'
field = ['name', 'url', 'city', 'tel',
         'address', 'time', 'intro', 'rate', 'review']


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2), reraise=True)
def try_get_url(j: int):
    element = browser.find_element(
        By.XPATH, f'/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[3]/div[{j}]/div[2]/dl/dt/a')
    return element


for idx in range(1, 2):
    for j in range(1, 16):
        city = 'phillipisland'
        writer, file = csvUtils.writeCSV(path, field)
        # URL
        element = try_get_url(j)
        url = element.get_attribute('href')

        # 进入里页
        element.click()
        browser.switch_to.window(browser.window_handles[1])

        # 名称
        title = browser.find_element(
            By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/div[1]/h1/a')
        title = title.text
        print(f'第{idx}页第{j}项::{title}')

        # 电话
        try:
            tel = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[2]/div[1]/ul/li[2]/span[2]')
            tel = tel.text
        except:
            tel = ''

        # 地址
        try:
            address = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[2]/div[1]/ul/li[1]/span[2]')
            address = address.text
        except:
            address = ''

        # 营业时间
        try:
            time = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[2]/div[1]/dl/dd')
            time = time.text
        except:
            time = ''

        # 简介
        try:
            intro = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[3]/div/div[1]/div/div')
            intro = intro.text
            if not (re.match('还没有人介绍', intro) == None):
                intro = ''
        except:
            intro = ''

        # 评分
        try:
            rate = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/ul/li[1]/span/b')
            rate = rate.text
        except:
            rate = ''

        # 点评
        try:
            review = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/ul/li[3]')
            review = review.text
            if not (re.match('你也游览', review) == None):
                review = ''
        except:
            review = ''

        writer.writerow({'name': title, 'url': url, 'city': city, 'tel': tel,
                        'address': address, 'time': time, 'intro': intro, 'rate': rate, 'review': review})
        csvUtils.closeCSV(file)
        # 退出里页
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
    # 每页爬取
    element = browser.find_element(
        By.XPATH, '/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[3]/div[16]/div/a[4]')
    element.click()
# 共116页
browser.quit()
