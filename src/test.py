import json
from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from utils.translator import translate_to_en_by_azure
from utils.distance import get_distance_by_bing,get_straight_distance,get_point_by_here
from tenacity import retry, wait_fixed, stop_after_attempt
from utils.str_util import check_str
import utils.csv_util as csvUtils

newfoodpath = r'data\\food.csv'

reader, reader_file, count = csvUtils.readCSV(newfoodpath)

for row in reader:
    coord=eval(row['Coord'])
    print(coord['lat'])