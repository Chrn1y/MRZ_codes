import base64
import io
from imageio import imread
from mrq_area import get_mrq_area
from mrz_decoding import get_mrz_data


def get_mrz_from_b64_bytes(data):
    b64_bytes = base64.b64encode(data)
    b64_string = b64_bytes.decode()
    img = imread(io.BytesIO(base64.b64decode(b64_string)))
    return get_mrz_data(get_mrq_area(img))