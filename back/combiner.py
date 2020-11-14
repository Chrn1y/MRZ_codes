import cv2
import base64
import io
from imageio import imread
from mrz_area import get_mrz_area
from mrz_decoding import get_mrz_data


def test_mrz(image):
    return get_mrz_data(get_mrz_area(image))
