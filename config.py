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
    },
    'richmenu': {
        'login': 'richmenu-1b9f083db5ccd8a902ce7254335ceb7c',
        'menu': 'richmenu-8e81db4e38d5e643d8152b92693ebb48'
    },
    'liff':{
        'login':'line://app/1653599527-KjlZpO3N',
        'edit':'line://app/1653599527-yzVX2E6N',
        'find':'line://app/1653599527-pVnjrOek',
        'comment':'line://app/1653599527-WBVGNDYv'
    },
    'domain':'https://42ef292e.ngrok.io/'
}

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}/{}?charset=utf8".format(
    config['mysql']['dialect'], config['mysql']['driver'], config['mysql']['username'], config['mysql']['password'], config['mysql']['host'], config['mysql']['database'])
