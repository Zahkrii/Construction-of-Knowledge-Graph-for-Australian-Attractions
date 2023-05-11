import time
from utils.translator import translate_to_en_by_azure
from utils.distance import get_geo_distance
import utils.csv_util as csvUtils
from itertools import combinations


path = 'data\\node.csv'
newpath = 'data\\newnode.csv'
field=['id1','coord1','distance','id2','coord2']

reader, reader_file, count = csvUtils.readCSV(path)

items=[{'id':row['ID'],'coord':eval(row['Coord'])} for row in reader]

for item1, item2 in combinations(items,2):
    writer, writer_file = csvUtils.writeCSV(newpath, field)
    dis=get_geo_distance(item1['coord'],item2['coord'])
    dis=round(dis,3)
    writer.writerow({'id1':item1['id'],'coord1':item1['coord'],'distance':dis,'id2':item2['id'],'coord2':item2['coord']})
    csvUtils.closeCSV(writer_file)
    time_str = time.strftime('%H:%M:%S', time.localtime(time.time()))
    print(f'[{time_str}] {item1["id"]}::{dis}km::{item2["id"]}')