import time
from utils.distance import get_point_by_bing, get_point_by_here
import utils.csv_util as csvUtils
from utils.lang_detect import judge_language
from utils.translator import translate_to_en_by_azure

foodpath = r'data\\working\\food_edit.csv'
hotelpath = r'data\\working\\hotels_edit.csv'
shoppath = r'data\\working\\shop_edit.csv'
sightpath = r'data\\working\\sights_edit.csv'

newfoodpath = r'data\\food.csv'
foodfield = ['RestaurantID:ID', 'Name', 'URL', 'Price', 'Dish', 'Tel', 'Address',
             'Time', 'Introduction', 'Special', 'Rate', 'Review', 'Coord', 'City', 'State', ':LABEL']
newhotelpath = r'data\\hotel.csv'
hotelfield = ['HotelID:ID', 'Name', 'URL', 'Tel',
              'Address', 'Price', 'Rate', 'Website', 'Coord', 'City', 'State', ':LABEL']
newshoppath = r'data\\shop.csv'
shopfield = ['ShopID:ID', 'Name', 'URL', 'Tel', 'Address',
             'Time', 'Introduction', 'Rate', 'Review', 'Coord', 'City', 'State', ':LABEL']
newsightpath = r'data\\sight.csv'
sightfield = ['SightID:ID', 'Name_CN', 'Name_EN', 'Address', 'Time',
              'Tel', 'Rate', 'Introduction', 'Tickets', 'Website', 'Coord', 'City', 'State', ':LABEL']
# 1
path = newhotelpath
# 2
field = hotelfield
# 3
reader, reader_file, count = csvUtils.readCSV(hotelpath)
idx = 1
for row in reader:
    addr = row['Address']
    if (judge_language(addr) == 'zh'):
        addr = translate_to_en_by_azure(addr)

    coord, address, city, state = get_point_by_here(addr)

    writer, writer_file = csvUtils.writeCSV(path, field)
    # 4
    writer.writerow({'HotelID:ID': row['HotelID:ID'], 'Name': row['Name'], 'URL': row['URL'], 'Price': row['Price'],
                     'Tel': row['Tel'], 'Address': address, 'Rate': row['Rate'], 'Website': row['Website'],
                     'Coord': coord, 'City': city, 'State': state, ':LABEL': row[':LABEL']})
    csvUtils.closeCSV(writer_file)
    time_str = time.strftime('%H:%M:%S', time.localtime(time.time()))
    # 5
    print(f'[{time_str}] 第{idx}项::{row["Name"]}::{coord}')
    idx += 1
csvUtils.createCSV(reader_file)
