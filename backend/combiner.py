import cv2
import base64
import io
from imageio import imread
from mrz_area import get_mrz_area
from mrz_decoding import get_json_mrz_data


def get_json_mrz(image):
    mrz_area = get_mrz_area(image)
    if mrz_area is None:
        return None
    data_json = get_json_mrz_data(mrz_area)
    if data_json is None:
        return None
    return data_json
