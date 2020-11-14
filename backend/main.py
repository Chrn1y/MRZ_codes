from flask import Flask, request, abort
from combiner import get_json_mrz
from PIL import Image
from io import BytesIO
import base64
import cv2
import numpy


app = Flask(__name__)

@app.route("/test")
def index():
    return '3228'


@app.route("/", methods=['POST'])
def image():
    image_str = request.get_json()['image']
    #print(image_str)
    image_orig = base64.b64decode(image_str)
    image_np = numpy.frombuffer(image_orig, dtype=numpy.uint8)
    image_cv2 = cv2.imdecode(image_np, flags=1)
    cv2.imshow('img', image_cv2)
    cv2.waitKey(0)
    print(image_cv2.shape)
    # print(test_mrz(image_cv2))
    response = get_json_mrz(image_cv2)
    if response is None:
        abort(418)
    return response


if __name__ == '__main__':
    app.run(port='8000', debug=True)
    # print(test_mrz())
