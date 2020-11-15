from flask import Flask, request, abort, Response
from combiner import get_json_mrz
import base64
import cv2
import numpy

app = Flask(__name__)


# requests POST with base64 picture
# returns jason with mrz and mrz transcription
@app.route("/", methods=['POST'])
def image():
    image_str = request.get_json()['image']
    image_orig = base64.b64decode(image_str)
    image_np = numpy.frombuffer(image_orig, dtype=numpy.uint8)
    image_cv2 = cv2.imdecode(image_np, flags=1)
    response = get_json_mrz(image_cv2)
    if response is None:
        abort(418)
    return Response(response, mimetype='application/json')


if __name__ == '__main__':
    app.run(port='8000')
