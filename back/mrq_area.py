import cv2

def getMrqArea(image): 
  '''
    Intput value - ndarray of (width, height, channels)
    Output value - ndarray of (width, height, channels) or None

    Function founds area of mrz code on the picture and returns it as image or 
    None if rmz area was not found
    
    Warning: 
    for appropriate results input picture should be orientated horizontally
  '''
  outputWidth = 800

  ratio = outputWidth / image.shape[0]
  resized = cv2.resize(image,None,fx=ratio,fy=ratio)


  blackWhite = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
  blackWhite = cv2.GaussianBlur(blackWhite, (3, 3), 0)


  blacked = cv2.morphologyEx(blackWhite, cv2.MORPH_BLACKHAT,
                             cv2.getStructuringElement(0, (15, 10)))

  closed = cv2.morphologyEx(blacked, cv2.MORPH_CLOSE,
                            cv2.getStructuringElement(0, (30,55)))

  otsu = cv2.threshold(closed, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

  squared = cv2.morphologyEx(otsu, cv2.MORPH_CLOSE,
                             cv2.getStructuringElement(0,(5,5)))

  eroded = cv2.erode(squared, cv2.getStructuringElement(0,(6,6)), 3)

  mrz = None
  contours = cv2.findContours(eroded.copy(), cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)[0]
  contours = sorted(contours, key=cv2.contourArea, reverse=True) 

  for c in contours:
    (x, y, w, h) = cv2.boundingRect(c)
    localWidth = w / float(h)
    globalWidth = w / float(resized.shape[1])

    if localWidth > 7 and globalWidth > 0.6:
      epsX = int((x + w) * 0.03)
      epsY = int((y + h) * 0.03)
      x -= epsX
      y -= epsY
      w += 2*epsX
      h += 2*epsY
      mrz = resized[y:y + h, x:x + w].copy()
      break

  return mrz
