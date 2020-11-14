import cv2
import base64
import io
from imageio import imread
from mrz_area import get_mrz_area
from mrz_decoding import get_mrz_data

def get_mrz_from_b64_bytes(data):
    b64_bytes = base64.b64encode(data)
    b64_string = b64_bytes.decode()
    img = imread(io.BytesIO(base64.b64decode(b64_string)))
    return get_mrz_data(get_mrz_area(img))


def test_mrz():
    return get_mrz_data(get_mrz_area(cv2.imread("./photo_2020-11-13_22-17-31.jpg")))
