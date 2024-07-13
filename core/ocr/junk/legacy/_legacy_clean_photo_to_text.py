import easyocr
from PIL import Image
import cv2
import sys, os

def search_text_easyocr(image):
  reader = easyocr.Reader(['ru', 'en'])
  results = reader.readtext(image)
  if len(results) == 0:
    return None
  #for bbox, text, prob in results:
    #print(f'Text: {text}, Probability: {prob:.4f}')
  print(' '.join(r[1] for r in results))
  bbox, text, prob = sorted(results, key=lambda x: x[-1])[-1]
  return bbox, text, prob

def makrup_recognized_text(image, bbox, text, prob):
  top_left = tuple(map(int, bbox[0]))
  bottom_right = tuple(map(int, bbox[2]))
  image = cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
  text_x_y = top_left[0], top_left[1] - 5
  image = cv2.putText(image, text, text_x_y, cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
  return image

def image_to_text(image):
  result = search_text_easyocr(image)
  if result is None:
    return '', image
  bbox, text, prob = result
  markup_image = makrup_recognized_text(image, bbox, text, prob)
  return text, markup_image

def read_image(img_filepath):
  return cv2.imread(img_filepath)

def save_image(image, filepath):
  cv2.imwrite(filepath, image)

def main():
  path_to_dir = sys.argv[1]
  for root, dirs, files in os.walk(path_to_dir):
    for file in files:
      src_img_filepath = os.path.join(root, file)
      if src_img_filepath.startswith('proc_'):
        continue
      _splt_src_filepath = list(os.path.split(src_img_filepath))
      _splt_src_filepath[-1] = 'proc_' + _splt_src_filepath[-1]
      markup_img_filepath = os.path.join(*_splt_src_filepath)
      print(f'{src_img_filepath=}')
      print(f'{markup_img_filepath=}')
      image = read_image(src_img_filepath)
      text, markup_image = image_to_text(image)
      save_image(markup_image, markup_img_filepath)
      print(text)


if __name__ == '__main__':
  main()

