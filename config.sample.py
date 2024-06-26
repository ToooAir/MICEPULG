config = {
    "LINE_CHANNEL_SECRET": "",
    "LINE_CHANNEL_ACCESS_TOKEN": "",
    "mysql": {
        "dialect": "mysql",
        "driver": "pymysql",
        "username": "",
        "password": "",
        "host": "",
        "database": "",
    },
    "richmenu": {"login": "", "menu": ""},
    "liff": "",
    "CLOUD_STORAGE_BUCKET": "tgif.momoka.tw",
    "default_avater": "https://storage.googleapis.com/tgif.momoka.tw/avatar/00.jpg",
    "allow_signup": True,
}

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}/{}?charset=utf8mb4".format(
    config["mysql"]["dialect"],
    config["mysql"]["driver"],
    config["mysql"]["username"],
    config["mysql"]["password"],
    config["mysql"]["host"],
    config["mysql"]["database"],
)

liffid = config["liff"].strip("line://app/")
