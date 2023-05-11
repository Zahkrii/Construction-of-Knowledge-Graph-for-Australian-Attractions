import utils.csv_util as csvUtils

path = 'data\sight.csv'

newpath = 'data\citys\states.csv'

field = ['SightID:ID', 'Name_CN', 'Name_EN', 'Address', 'Time',
         'Tel', 'Rate', 'Introduction', 'Tickets', 'Website', 'Coord', 'City', 'State', ':LABEL']

newfield = ['PlaceID:ID', 'Name', ':LABEL']

label = 'City/Region'

prefix = 'place_'

reader, reader_file, count = csvUtils.readCSV(path)

idx = 1
for row in reader:
    reader2, reader_file2, count2 = csvUtils.readCSV(newpath)
    flag = False
    for item in reader2:
        if (row['City'] == item['Name']):
            flag = True
            break
    csvUtils.closeCSV(reader_file2)
    if (not (flag)):
        # 打开文件
        writer, file = csvUtils.writeCSV(newpath, newfield)
        writer.writerow({'PlaceID:ID': f'{prefix}{idx:0>4d}',
                         'Name': row['City'], ':LABEL': label})
        csvUtils.closeCSV(file)
        print(f'{prefix}{idx:0>3d}::{row["City"]}')
        idx += 1

csvUtils.closeCSV(reader_file)
