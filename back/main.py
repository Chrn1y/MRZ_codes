from flask import Flask

app = Flask(__name__)


@app.route("/image")
def image():
    return 0


if __name__ == '__main__':
    app.run()