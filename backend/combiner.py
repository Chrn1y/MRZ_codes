import cv2
import base64
import io
from imageio import imread
from mrz_area import get_mrz_area
from mrz_decoding import mrz_transcript


def get_json_mrz(image):
    mrz_area = get_mrz_area(image)
    if mrz_area is None:
        return None

    # cv2.imshow("area", mrz_area)
    # cv2.waitKey(0)

    data_json = mrz_transcript(mrz_area)
    if data_json is None:
        return None
    return data_json


def test_mrz():
    return get_json_mrz(cv2.imread("./working_test2.jpg"))
