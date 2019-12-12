import csv

import alchemyFunc

from config import config

with open("/var/www/tgif.momoka.tw/user_data.csv", "r", encoding="utf8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        alchemyFunc.importUser(**row) 