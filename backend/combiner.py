from mrz_area import get_mrz_area
from mrz_decoding import mrz_transcript


# call functions one by one
# get image return json or None
def get_json_mrz(image):
    mrz_area = get_mrz_area(image)
    if mrz_area is None:
        return None
    data_json = mrz_transcript(mrz_area)
    if data_json is None:
        return None
    return data_json

