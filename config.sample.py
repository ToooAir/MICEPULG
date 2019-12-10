config = {
    'LINE_CHANNEL_SECRET': '',
    'LINE_CHANNEL_ACCESS_TOKEN': '',
    'mysql': {
        'dialect': 'mysql',
        'driver': 'pymysql',
        'username': '',
        'password': '',
        'host': '',
        'database': ''
    },
    'richmenu': {
        'login': '',
        'menu': ''
    },
    'liff':{
        'login':'',
        'edit':'',
        'find':'',
        'comment':''
    },
    'domain':'https://d7cac9a9.ngrok.io/'
}

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}/{}?charset=utf8".format(
    config['mysql']['dialect'], config['mysql']['driver'], config['mysql']['username'], config['mysql']['password'], config['mysql']['host'], config['mysql']['database'])