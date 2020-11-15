# MRZ codes extraction 

This project provides both algorithm and UI for [MRZ](https://en.wikipedia.org/wiki/Machine-readable_passport) code extraction. You may use only API or just take a picture in the android mobile phone app and it will be sent to the server where the main algorithm extracts and deciphers MRZ code.

* [Backend](#backend)
  * [Getting started](#getting-started)
  * [Run](###Run)
* [API Reference](#api-reference)
* [Android app](#android-app)
  * [Installation](#installation)
  * [How to use](#how-to-use)
* [MRZ area detection module](#mrz-area-detection-module)
  * [Description](#description1)
* [MRZ recognition module](#mrz-recognition-module)
  * [Description](#description2)

## <a name="backend"> Backend </a>

### <a name="getting-started"> Getting started </a>

First of all, install virtualenv:

```python
python3 -m pip install virtualenv
```

Clone repo and install all the modules:

```python
git clone git@github.com:Chrniy/MRZ_codes.git
cd MRZ_codes/backend

python3 -m virtualenv mrz_env
source mrz_env/bin/activate
# or 
# cd mrz_env/Scripts
# activate.bat
# cd ../..
pip install -r requirements.txt
```

```python
python3 -m virtualenv mrz_env
source env/bin/activate
pip install -r requirements.txt
```

Install [ngrok](https://ngrok.com/download)

Install [Tesseract OCR](https://github.com/tesseract-ocr/tessdoc) and paste the path to tesseract_cmd in backend/setup.py like this:

```python
PATH_TO_TESSERACT = r'C:\Users\artyo\AppData\Local\Tesseract-OCR\tesseract.exe'
```

Also put mrz.traineddata file in trainedata folder which is located in the same folder as tesseract_cmd on your machine

### <a name="run"> Run </a>

Run ngrok locally to publish 8000 port with http

```python
ngrok http 8000
```

Run main.py script 

```python
cd MRZ_codes/backend

source mrz_env/bin/activate
# or 
# cd mrz_env/Scripts
# activate.bat
# cd ../..
python3 ./main.py
```

## <a name="api-reference"> API Reference </a>

We have only one function that receives POST request with base64 encoded image in JSON field "image" (`content-type = application/json`) and returns JSON with decoded MRZ (`content-type = application/json`)

Example of response:

```json
{
    "surname": "VOROPAEVA", 
    "name": "ALEKSANDRA", 
    "country": "Germany", 
    "nationality": "RUS", 
    "birth_date": "1991-05-08", 
    "expiry_date": "2014-10-30", 
    "sex": "F", 
    "document_type": "VD", 
    "document_number": "047286890", 
    "optional_data": "TM<<1028", 
    "birth_date_hash": "9", 
    "expiry_date_hash": "9", 
    "document_number_hash": "6", 
  	"mrz_code": "VDD<<VOROPAEVA<<ALEKSANDRA<<<<<<<<<<\n0472868906RUS9105089F1410309TM<<1028"
}
```

## <a href="android-app"> Android app </a>

### <a href="installation"> Installation </a>

Install `mrz_cam.apk` and give it all permissions it asks

### <a href="how-to-use"> How to use </a>

When you are ready, press `Начать сканирование` and take a picture horisontaly, like it is shown below:

![image-20201115041325464](https://sun9-57.userapi.com/DZouBNMEfIC7jvmK4C8efXseSEYNtxrz7BQ_Fw/-KvS2O2zMyg.jpg)

Wait for the server to answer

There could be several different responses:

* `Приложение не обнаружило MRZ, рекомендуем повторить сканирование горизонтально` – in this case you should try to retake the photo
* `Сервер не отвечает или введен невалидный ключ` – in this case you should check validness of your http/ngrok key or viability of the server
* Correct data – enjoy

## <a href="mrz-area-detection-module"> MRZ area detection module </a>

This module detects the machine readable code in the picture of a document and extracts it as an image. In order to get proper results, the input image should be orientated.



		**Input value:** ndarray of shape (height, weight, channels)
	
		**Output value:** ndarray of shape (height, weight, channels) or None (if area was not found)



Note: this module requires [OpenCV](https://opencv.org/) library for python

#### <a name="description1"> Description </a>

Algorithm is based on OpenCV morphological transformations. The following transformations were used:

* *Color space conversion* – improves work of the next layers
* *Blackhat* – highlights letters and make background black
* *Closing* – increases borders of elements and blures them,  by that letter lines become rectangles
* *Thresholding, Otsu method* – divides all color tones by only black and white colors
* *Erosion* – deletes small noise dots or horizontal lines

After applying these transformations we get a black/white picture where all close letters are represented as rectangles or their combinations. 

On the next stage we use OpenCV function getCounters to get all counters that it is possible to find. Found counters are sorted in ascending order, so that we can find which one stands for RMZ. As RMZ is usually a long and narrow rectangle, we analyze these features and choose the most suitable one.

Example of found area (red):

![image-20201115040010337](https://sun9-50.userapi.com/44cG0_gmsG9q0FQg8EK0tT6jZT_L-4PiWnHoXQ/mponB8T54SE.jpg)

Example of output:

![image-20201115040038305](https://sun9-73.userapi.com/jaSr1SusdYWLWP5I-nP4MYCbj6GMHNfnI1gwcg/uPULGrFygcM.jpg)



## <a href="mrz-recognition-module"> MRZ recognition module </a>

This module extracts MRZ code from the MRZ area image and transforms it to JSON format. Transformation algorithm depends on the document type. Supported formats are Td1, Td2, Td3, international passport, MRVA  and MRVB.



		**Input value:** ndarray of shape (height, weight, channels)
		**Output value:** JSON dictionary or None (if algorithm did not manage to transcript the image)



#### <a name="description2"> Description </a>

This algorithm is based on Google Tesseract image text recognition, OpenCV morphological transformations and mrz decoding algorithm implemented by this [Github user](https://github.com/Arg0s1080/mrz).

In order to get JSON output you should call `get_transcription()` function. It calls `get_image_variants()` that provides a list of images with different OpenCV transformations and `get_mrz_data()` that gets mrz code from every image and tries to sequentially transform it with provided algorithms for different document types.

Example:

![image-20201115042028332](https://sun9-63.userapi.com/wMfKLAQHMRkRZdjX2t2c7VASKK3H4_uwxsamxQ/yr_puaJ2ZZE.jpg)
