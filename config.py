config = {
    'LINE_CHANNEL_SECRET': 'd8a47b4945f4d8ca660b5b732259af5e',
    'LINE_CHANNEL_ACCESS_TOKEN': 'rV7RixnxnKPN60jw7mQY9/zL9mGpGQzqPD1D15no/cZzaA9ms3AP67D1dds00U5sPkCk5UoGJyAk9mHZMnK6aom0PTUZpBjMhV5FACGUTFETUSm6mH1FNUJmAtjZLKlr1VBZP5ABwrKha0K0tGkhXAdB04t89/1O/w1cDnyilFU=',
    'mysql': {
        'dialect': 'mysql',
        'driver': 'pymysql',
        'username': 'line',
        'password': 'linepw',
        'host': 'localhost',
        'database': 'lineDB'
    }
}

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}/{}?charset=utf8".format(
    config['mysql']['dialect'], config['mysql']['driver'], config['mysql']['username'], config['mysql']['password'], config['mysql']['host'], config['mysql']['database'])

