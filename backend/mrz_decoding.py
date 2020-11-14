import pytesseract
from mrz.checker.td1 import TD1CodeChecker as checker1
from mrz.checker.td2 import TD2CodeChecker as checker2
from mrz.checker.td3 import TD3CodeChecker as checker3
from mrz.checker.mrva import MRVACodeChecker as checkerA
from mrz.checker.mrvb import MRVBCodeChecker as checkerB
from mrz.base.countries_ops import get_country
import json
import cv2
import datetime
import numpy as np

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
    decoded_data = None;

    for decoder in decoders:
        try:
            decoded_data = decoder(mrz_code)
        except:
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


def get_mrz_from_image(image):
    '''
    return images mrz code
    return type - string
    '''
    return pytesseract.image_to_string(image, lang="mrz")


def get_mrz_data(image):
    '''
    return decoded_mrz_data
    return type - dict
    return None if decoding is impossible
    '''
    mrz_code = get_mrz_from_image(image).replace(' ', '').strip()
    decoded_data = decode_mrz(mrz_code)
    if decoded_data is None:
        return None
    decoded_data['mrz_code'] = mrz_code
    return convert_data(decoded_data)


def get_blacked(image):
    '''
    return blacked image
    return type - 3d list
    '''
    bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rectker = cv2.getStructuringElement(0, (15, 10))
    return cv2.morphologyEx(bw, cv2.MORPH_BLACKHAT, rectker)


def make_contrast(image, alpha):
    '''
    return contrast image
    return type - 3d list
    '''
    return cv2.convertScaleAbs(image, alpha=alpha)


def make_erode(image):
    '''
    return eroded image
    return type - 3d list
    '''
    return cv2.erode(image, cv2.getStructuringElement(0, (2, 2)), 2)


def get_image_variants(image):
    '''
    return different variants of image transformation
    return type - list of images - 4d array
    '''
    blacked = get_blacked(image)
    eroded_image = make_erode(image)
    eroded_blacked = make_erode(blacked)

    variants = [blacked, eroded_image, eroded_blacked]
    for alpha in np.arange(1, 3.1, 0.5):
        image_contrast = make_contrast(image, alpha=alpha)
        blacked_contract = make_contrast(blacked, alpha)
        # eroded_image_contrast = make_erode(image_contrast)
        # eroded_image_contrast
        eroded_blacked_contract = make_erode(image_contrast)

        variants.extend([image_contrast, blacked_contract, eroded_blacked_contract])
    return variants


def mrz_transcript(image):
    '''
    tries to decode image and its different variation
    return json decoded data
    return None if decoding is impossible
    '''
    try:
        variants = get_image_variants(image)
        for variant in variants:
            data = get_mrz_data(variant)
            if data is not None:
                return json.dumps(data)
    except:
        pass
    return None
