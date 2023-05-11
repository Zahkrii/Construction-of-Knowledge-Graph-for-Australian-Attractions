import random
import time
import requests
from lxml import etree
from fake_useragent import UserAgent


def getHTML(url: str, isSleep: bool = True):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'referer': 'https://cn.bing.com/',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }
    res = requests.get(url=url, headers=headers)
    if (isSleep == True):
        time.sleep(random.uniform(0.8, 4.2))
    html = etree.HTML(res.text)
    return html


def xpath(html, xpath: str):
    res = html.xpath(xpath)
    if (res):
        return res[0]
    else:
        return ''


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def getHTMLbyProxy(url: str, isSleep: bool = True):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'referer': 'https://cn.bing.com/',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            # 使用代理访问
            res = requests.get(
                url, proxies={"http": "http://{}".format(proxy)}, headers=headers)
            if (isSleep == True):
                time.sleep(random.uniform(0.8, 3.2))
            html = etree.HTML(res.text)
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    return None
