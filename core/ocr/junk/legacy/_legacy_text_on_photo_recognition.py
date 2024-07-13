from PIL import Image
import cv2
import numpy as np
import os

def read_image(img_filepath):
  return cv2.imread(img_filepath)

def preproc(image):
  # Конвертация изображения в оттенки серого
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # Бинаризация изображения методом Otsu
  _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
  # Удаление шума с использованием морфологических операций
  kernel = np.ones((1, 1), np.uint8)
  binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
  binary_image = cv2.medianBlur(binary_image, 3)
  return binary_image

def preproc2(image):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # Увеличение разрешения
  gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
  # Увеличение контраста и яркости
  alpha = 1.5  # Контраст (1.0-3.0)
  beta = 0     # Яркость (0-100)
  gray = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
  # Адаптивная бинаризация изображения
  binary_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
  # Удаление шума
  binary_image = cv2.medianBlur(binary_image, 3)
  return binary_image

def search_text_tesseract_ocr(image):
  import pytesseract
  #image = Image.open(img_filepath)
  image = Image.fromarray(image)
  text = pytesseract.image_to_string(image, lang='rus')
  return text

def search_text_easyocr(image):
  import easyocr
  import matplotlib.pyplot as plt
  '''
  plt.imshow(image, cmap='gray')
  plt.show()
  '''
  reader = easyocr.Reader(['ru', 'en'])
  results = reader.readtext(image)
  if len(results) == 0:
    print('Not found.')
    return '', None
  for bbox, text, prob in results:
    print(f'Text: {text}, Probability: {prob:.4f}')

  bbox, text, prob = sorted(results, key=lambda x: x[-1])[-1]
  top_left = tuple(map(int, bbox[0]))
  bottom_right = tuple(map(int, bbox[2]))
  image = cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
  text_x_y = top_left[0], top_left[1] - 5
  #image = cv2.putText(image, text, top_left, cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
  image = cv2.putText(image, text, text_x_y, cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
  return text, image

def search_text_paddle_ocr(image):
  from paddleocr import PaddleOCR, draw_ocr
  ocr = PaddleOCR(use_angle_cls=True, lang='ru')
  result = ocr.ocr(image, cls=True)
  for line in result:
    for bbox, (text, prob) in line:
      print(f'Text: {text}, Probability: {prob:.4f}')
  return ''

def image_to_text(img_filepath):
  from pathlib import Path
  p = Path(img_filepath)
  p = os.path.join(p.parent,'proc_' + p.name)

  image = read_image(img_filepath)
  #image = preproc(image)
  #image = preproc2(image)
  #txt = search_text_tesseract_ocr(image)
  txt, image = search_text_easyocr(image)
  if image is not None:
    cv2.imwrite(p, image)
    print(f'{p=}')
  #txt = search_text_paddle_ocr(image)
  return txt

if __name__ == '__main__':
  '''
  t = image_to_text('frame_258.jpg')
  print(t)
  exit()
  '''
  import sys
  path_to_dir = sys.argv[1]
  for root, dirs, files in os.walk(path_to_dir):
    for file in files:
      filepath = os.path.join(root, file)
      print(f'{filepath=}')
      txt = image_to_text(filepath)
      print(txt)

