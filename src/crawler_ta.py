from tqdm import tqdm
import utils.csv_util as csvUtils
import utils.html as htmlUtils

path = csvUtils.createCSV('tripa/sights/all.csv', ('name', 'url',
                          'time', 'website', 'ticket', 'review', 'address_raw', 'about'))


def getData(index: int):
    sight_name = htmlUtils.xpath(html,
                                 f'/html/body/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/div/div/section[{index}]/div/div/div/article/div[2]/header/div/div/a[1]/h3/div/span/div/text()')
    sight_url = htmlUtils.xpath(html,
                                f'/html/body/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/div/div/section[{index}]/div/div/div/article/div[2]/header/div/div/a[1]/@href')
    deeper(sight_name, sight_url)


def deeper(name: str, url: str):
    html_deep = htmlUtils.getHTML(url)
    sight_open_time = htmlUtils.xpath(html_deep,
                                      '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[1]/div/div/div/div/div[2]/div[1]/div/div/span/text()')
    sight_website = htmlUtils.xpath(html_deep,
                                    '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[1]/div/div/div/div/div[2]/div[3]/a[1]/@href')
    sight_ticket = htmlUtils.xpath(html_deep,
                                   '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[2]/div/div/div/div[1]/div[2]/div/div/div[1]/div[2]/text()')
    sight_reviews = htmlUtils.xpath(html_deep,
                                    '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[8]/div/div/div/section/section/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/text()')
    sight_address_raw = htmlUtils.xpath(html_deep,
                                        '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[5]/div/div/div[2]/div[1]/div/div/div/div[3]/ul/li/div/text()')
    sight_about = htmlUtils.xpath(html_deep,
                                  '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div/text()')
    writer, file = csvUtils.writeCSV(path, ['name', 'url',
                                            'time', 'website', 'ticket', 'review', 'address_raw', 'about'])
    writer.writerow({'name': name, 'url': url, 'time': sight_open_time, 'website': sight_website,
                    'ticket': sight_ticket, 'review': sight_reviews, 'address_raw': sight_address_raw, 'sight_about': sight_about})
    csvUtils.closeCSV(file)


for j in tqdm(range(0, 300)):
    print(f'starting page {j}.')
    html = htmlUtils.getHTML(
        f'https://www.tripadvisor.com/Attractions-g255055-Activities-oa{0+j*30}-Australia.html')
    #1-3
    for index in range(2, 5):
        getData(index)
    #4-6
    for index in range(6, 9):
        getData(index)
    #7-9
    for index in range(10, 13):
        getData(index)
    #10-12
    for index in range(14, 17):
        getData(index)
    #13-16
    for index in range(18, 22):
        getData(index)
    print(f'page {j} half done.')
    #17-20
    for index in range(23, 27):
        getData(index)
    #21-24
    for index in range(28, 32):
        getData(index)
    #25-28
    for index in range(33, 37):
        getData(index)
    #29-30
    for index in range(38, 40):
        getData(index)
    print(f'page {j} done.')