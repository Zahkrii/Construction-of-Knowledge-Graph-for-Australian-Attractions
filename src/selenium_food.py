from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import utils.csv_util as csvUtils

service = Service(executable_path='driver\msedgedriver.exe')

options = webdriver.EdgeOptions()
options.add_argument('blink-settings=imagesEnabled=false')

browser = webdriver.Edge(service=service, options=options)

browser.get('https://you.ctrip.com/restaurantlist/Australia100048/list-p102.html')

path = r'ctrip\\food\\food.csv'
field = ['name', 'url', 'price', 'dishes', 'tel',
         'address', 'time', 'intro', 'special', 'rate', 'review']

for idx in range(102, 117):
    for j in range(1, 16):
        writer, file = csvUtils.writeCSV(path, field)
        # URL
        element = browser.find_element(
            By.XPATH, f'/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[3]/div[{j}]/div[3]/dl/dt/a')
        url = element.get_attribute('href')

        # 进入里页
        element.click()
        browser.switch_to.window(browser.window_handles[1])

        # 名称
        title = browser.find_element(
            By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/div[1]/h1')
        title = title.text
        print(f'第{idx}页第{j}项::{title}')
        # 价格
        try:
            price = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[2]/div[1]/ul/li[1]/span[2]/em')
            price = price.text
        except:
            price = ''

        # 菜系
        try:
            dish = browser.find_elements(
                By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[2]/div[1]/ul/li[2]/span[2]/dd/child::a')
            dishes = []
            for d in dish:
                dishes.append(d.text)
            dishes = ','.join(dishes)
        except:
            dishes = ''

        # 电话
        try:
            tel = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[2]/div[1]/ul/li[3]/span[2]')
            tel = tel.text
        except:
            tel = ''

        # 地址
        try:
            address = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[2]/div[1]/ul/li[4]/span[2]')
            address = address.text
        except:
            address = ''

        # 营业时间
        try:
            time = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[2]/div[1]/ul/li[5]/span[2]')
            time = time.text
        except:
            time = ''

        # 简介
        try:
            intro = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[3]/div[1]/div[1]')
            intro = intro.text
            if not (re.match('还没有人介绍', intro) == None):
                intro = ''
        except:
            intro = ''

        # 特色菜
        try:
            special = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[3]/div[1]/div[2]/p')
            special = special.text
        except:
            special = ''

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
        except:
            review = ''

        writer.writerow({'name': title, 'url': url, 'price': price, 'dishes': dishes, 'tel': tel,
                        'address': address, 'time': time, 'intro': intro, 'special': special, 'rate': rate, 'review': review})
        csvUtils.closeCSV(file)
        # 退出里页
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
    # 每页爬取
    element = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[3]/div[16]/div/a[7]')
    element.click()
# 共116页
browser.quit()
