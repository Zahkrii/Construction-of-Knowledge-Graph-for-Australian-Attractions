import time
import re
from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import utils.csv_util as csvUtils
from utils.str_util import check_str
from tenacity import retry, wait_fixed, stop_after_attempt

service = Service(executable_path='driver\msedgedriver.exe')

options = webdriver.EdgeOptions()
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('log-level=3')

browser = webdriver.Edge(service=service, options=options)

browser.get(
    'https://www.tripadvisor.com.au/Hotels-g255335-Coolangatta_Gold_Coast_Queensland-Hotels.html')

path = r'ctrip\\hotels\\08.hotel_other.csv'
city = 'Coolangatta'

startidx = 1
endidx = 2

field = ['name', 'url', 'city', 'tel', 'address', 'price', 'rate', 'website']


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2), reraise=True)
def try_get_item():
    elements = browser.find_elements(
        By.CSS_SELECTOR, 'div[class="jsTLT K"] > a')
    return elements

"""
WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(
    (By.XPATH, '/html/body/div[1]/main/div[3]/div/div[2]/div/div[1]/div[2]/div[3]/div/div[13]/div/button'))).click()
"""
time.sleep(15)

for idx in range(startidx, endidx):
    # 获取列表元素
    elements = try_get_item()
    j = 1
    for ele in elements:
        # 去除无效内容
        if (not (check_str('\d{1,2}. ', ele.text))):
            continue

        writer, file = csvUtils.writeCSV(path, field)

        # 链接
        url = ele.get_attribute('href')

        # 切换标签
        browser.execute_script(f'window.open("{url}")')
        browser.switch_to.window(browser.window_handles[1])

        time.sleep(1)
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # 名称
        title = browser.find_element(By.ID, 'HEADING').text

        print(f'第{idx}页第{j}项::{title}')

        # 价格
        try:
            price = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[6]/div/div/div[1]/div[1]/div[1]/div[2]/div/div')
            price = price.text
        except:
            try:
                price = browser.find_element(
                    By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[6]/div/div/div[1]/div[2]/a/div[1]/div[2]/div')
                price = price.text
            except:
                price = ''

        # 电话
        try:
            tel = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[1]/div/div[6]/div/div/div/div[2]/div/div[2]/div/div[2]/div/a/span[2]')
            tel = tel.text
        except:
            tel = ''

        # 地址
        try:
            address = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[1]/div/div[6]/div/div/div/div[2]/div/div[2]/div/div[1]/div/span[2]/span')
            address = address.text
        except:
            address = ''

        # 评分
        try:
            rate = browser.find_element(
                By.CSS_SELECTOR, '#ABOUT_TAB > div.ui_columns.MXlSZ > div:nth-child(1) > div.grdwI.P > span')
            rate = rate.text
        except:
            rate = ''

        # 网站
        try:
            website = browser.find_element(
                By.XPATH, '/html/body/div[2]/div[1]/div/div[6]/div/div/div/div[2]/div/div[2]/div/div[3]/div/a')
            website = website.get_attribute('href')
        except:
            website = ''

        writer.writerow({'name': title, 'url': url, 'city': city, 'tel': tel,
                        'address': address, 'price': price, 'rate': rate, 'website': website})
        csvUtils.closeCSV(file)
        # 退出里页
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        j += 1
        if(j>=15):
            break
    # 每页爬取
    elements = browser.find_elements(
        By.CSS_SELECTOR, 'a[class="BrOJk u j z _F wSSLS tIqAi unMkR"]')
    if (len(elements) > 1):
        elements[1].click()
    else:
        elements[0].click()
    time.sleep(3)
# 共116页
browser.quit()
