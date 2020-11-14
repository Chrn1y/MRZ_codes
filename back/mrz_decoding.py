import pytesseract
from mrz.checker.td3 import TD3CodeChecker, get_country
import json
from setup import PATH_TO_tesseract

pytesseract.pytesseract.tesseract_cmd = PATH_TO_tesseract


def convert_to_date(string):
    return ".".join([string[-2:], string[2:-2], string[:2]])


def to_json(fields):
    data = {}
    fieldsName = ['surname', 'name', 'country',
                  'nationality', 'birth_date',
                  'expiry_date', 'sex', 'document_type',
                  'document_number', 'optional_data']
    for i, key in enumerate(fieldsName):
        data[key] = fields[i]
    data['country'] = get_country(data['country'])
    data['birth_date'] = convert_to_date(data['birth_date'])
    data['expiry_date'] = convert_to_date(data['expiry_date'])
    return json.dumps(data)


def get_mrz_data(image):
    mrz_code = pytesseract.image_to_string(image, lang="mrz")[:-2]
    td3_check = TD3CodeChecker(mrz_code)
    fields = td3_check.fields()

    return to_json(fields)
