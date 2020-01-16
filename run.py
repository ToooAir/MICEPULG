from flask import Flask

from view.liff import liff
from view.message import message

app = Flask(__name__)
app.register_blueprint(message)
app.register_blueprint(liff)

if __name__ == "__main__":
    app.run()
