from flask import Flask, request
from mrq_area import get_mrz_from_b64_bytes

app = Flask(__name__)


@app.route("/")
def image():
    img64 = request.get_json()["image"]
    get_mrz_from_b64_bytes(img64)


if __name__ == '__main__':
    app.run()