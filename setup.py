import csv

import alchemyFunc

from config import config

with open("/Users/linroex/Downloads/資料總表 - 工作表1 (1).csv", "r", encoding="utf8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        alchemyFunc.importUser(**row) 