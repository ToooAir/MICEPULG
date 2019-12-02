config = {
    'LINE_CHANNEL_SECRET': '31e924342ffa2bce12c004b1d6a1d611',
    'LINE_CHANNEL_ACCESS_TOKEN': 'OsZl/cGwEraPJmbK3TuJfxioXJ0vZ4v7XeQBSUVt1qZzyVA7GqUftQhZR6sxO7XJbfHvm2vS4X02EXSoFHmdkMX36dLn8y9EqPlh8UrA3G+2LU2z846zvwpmWqqV8udc8P8e/pPCBPhO1AzY7qu/iAdB04t89/1O/w1cDnyilFU=',
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

