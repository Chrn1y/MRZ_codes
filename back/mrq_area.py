import cv2
from numpy import array
import base64
import io
from imageio import imread


def get_mrz_from_b64_bytes(data):
    b64_bytes = base64.b64encode(data)
    b64_string = b64_bytes.decode()
    img = imread(io.BytesIO(base64.b64decode(b64_string)))
    getMrqArea(img)


def getMrqArea(image):
    blackWhite = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blackWhite = cv2.GaussianBlur(blackWhite, (3, 3), 0)
    blacked = cv2.morphologyEx(blackWhite, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(0, (14, 6)))
    closed = cv2.morphologyEx(blacked, cv2.MORPH_CLOSE, cv2.getStructuringElement(0, (30, 30)))
    otsu = cv2.threshold(closed, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    squared = cv2.morphologyEx(otsu, cv2.MORPH_CLOSE, cv2.getStructuringElement(0, (30, 30)))
    eroded = cv2.erode(squared, cv2.getStructuringElement(0, (5, 5)), 3)

    contours = cv2.findContours(eroded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        localWidth = w / float(h)
        globalWidth = w / float(image.shape[1])

        if localWidth > 3 and globalWidth > 0.15:
            epsX = int((x + w) * 0.03)
            epsY = int((y + h) * 0.03)
            x -= epsX
            y -= epsY
            w += 2 * epsX
            h += 2 * epsY
            rmz = image[y:y + h, x:x + w].copy()
            break

    return rmz
