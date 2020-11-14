from flask import Flask, request
from combiner import get_mrz_from_b64_bytes, test_mrz

app = Flask(__name__)


@app.route("/")
def image():
    img64 = request.get_json()["image"]
    get_mrz_from_b64_bytes(img64)


if __name__ == '__main__':
    app.run()