import csv
from io import TextIOWrapper


def createCSV(path: str, header: tuple = ('col1', 'col2')):
    file = open(path, 'a+', newline='', encoding='utf-8-sig')
    writer = csv.writer(file)
    writer.writerow(header)
    file.close()
    return path


def readCSV(path: str):
    file = open(path, 'r', newline='', encoding='utf-8-sig')
    filelines = len(open(path, 'r', newline='', encoding='utf-8-sig').readlines())
    reader = csv.DictReader(file)
    return reader, file, filelines-1


def writeCSV(path: str, fieldnames: list = ['col1', 'col2']):
    file = open(path, 'a', newline='', encoding='utf-8-sig')
    writer = csv.DictWriter(file, fieldnames)
    return writer, file


def closeCSV(file: TextIOWrapper):
    file.close()
