import pytesseract
from mrz.checker.td3 import TD3CodeChecker, get_country
from mrz.checker.td1 import TD1CodeChecker as checker1
from mrz.checker.td2 import TD2CodeChecker as checker2
from mrz.checker.td3 import TD3CodeChecker as checker3
from mrz.checker.mrva import MRVACodeChecker as checkerA
from mrz.checker.mrvb import MRVBCodeChecker as checkerB
from mrz.base.countries_ops import get_country
import json
import cv2
import datetime

from setup import PATH_TO_tesseract

pytesseract.pytesseract.tesseract_cmd = PATH_TO_tesseract


def decode_td1(mrz_code):
    '''
    decode type1 travel document
    '''
    checked = checker1(mrz_code)
    return dict(checked.fields()._asdict())


def decode_td2(mrz_code):
    '''
    decode type2 travel document
    '''
    checked = checker2(mrz_code)
    return dict(checked.fields()._asdict())


def decode_td3(mrz_code):
    '''
    decode type3 travel document == international passport
    '''
    checked = checker3(mrz_code)
    return dict(checked.fields()._asdict())


def decode_mrvA(mrz_code):
    '''
    decode visa type A
    '''
    checked = checkerA(mrz_code)
    return dict(checked.fields()._asdict())


def decode_mrvB(mrz_code):
    '''
    decode visa type B
    '''
    checked = checkerB(mrz_code)
    return dict(checked.fields()._asdict())


def decode_mrz(mrz_code):
    '''
    Decodes mrz_code for different documents types.
    return None if decoding is impossible.
    '''
    decoders = [decode_td1, decode_td2, decode_td3, decode_mrvA, decode_mrvB]
    decoded_data = None

    for decoder in decoders:
        try:
            decoded_data = decoder(mrz_code)
        except:
            # Я не нашел у ошибок mrz общего предка чтобы ловить
            pass

    return decoded_data


def to_date(date):
    return datetime.datetime.strptime(date, '%y%m%d').strftime('%Y-%m-%d')


def convert_data(data):
    '''
    convert dates to %Y-%m-%d format
    convert country_code to country name
    '''
    data['country'] = get_country(data['country'])
    data['birth_date'] = to_date(data['birth_date'])
    data['expiry_date'] = to_date(data['expiry_date'])
    return data


def get_mrz_from_image(image) :
  return pytesseract.image_to_string(image, lang="mrz")


def get_json_mrz_data(image):
  mrz_code = get_mrz_from_image(image).replace(' ', '').strip()
  decoded_data = decode_mrz(mrz_code)
  if decoded_data is None:
    return None
  return json.dumps(convert_data(decoded_data))
