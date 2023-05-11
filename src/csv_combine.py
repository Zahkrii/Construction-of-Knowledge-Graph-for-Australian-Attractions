import utils.csv_util as csvUtils
import os,csv


def get_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


path = r'ctrip\\sights\\index'

new_file_path=r'ctrip\\sights\\index.csv'

newfile = open(new_file_path, 'a+', newline='', encoding='utf-8-sig')
writer = csv.writer(newfile)

for file in get_files(path):
    print(file)
    reader, reader_file, count = csvUtils.readCSV(f'{path}\\{file}')
    for row in reader:
        newurl=row['url'][21:]
        writer.writerow((row['sight'],newurl))
    csvUtils.closeCSV(reader_file)
newfile.close()
