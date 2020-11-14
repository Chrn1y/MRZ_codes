from flask import Flask, request
from combiner import get_mrz_from_b64_bytes, test_mrz

app = Flask(__name__)


@app.route("/")
def index():
    return '3228'


@app.route("/image", methods=['POST'])
def image():
    img64 = request.get_json()["image"]
    print(img64)
    # get_mrz_from_b64_bytes(img64)
    return '1337'


if __name__ == '__main__':
    app.run(port='8000', debug=True)
    # print(test_mrz())
