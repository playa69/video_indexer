import easyocr
from PIL import Image
import cv2

def read_image_from_file(img_filepath):
  return cv2.imread(img_filepath)

def compress_and_process_image(image, width=None, height=None, quality=85):
  # Получение оригинальных размеров изображения
  original_height, original_width = image.shape[:2]
  # Изменение размера изображения, если указаны новые размеры
  if width and height:
      new_size = (width, height)
  elif width:
      ratio = width / float(original_width)
      new_size = (width, int(original_height * ratio))
  elif height:
      ratio = height / float(original_height)
      new_size = (int(original_width * ratio), height)
  else:
      new_size = (original_width, original_height)
  resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
  # Преобразование изображения в формат, используемый OpenCV
  # In this example, we set custom encoding parameters using a list of integers. The cv2.IMWRITE_JPEG_QUALITY parameter sets the quality of the JPEG compression, with a value between 0 (lowest quality, highest compression) and 100 (highest quality, lowest compression). We set the quality to 90, which results in a higher-quality output image compared to the default value of 95.
  _, compressed_image = cv2.imencode('.jpg', resized_image, [cv2.IMWRITE_JPEG_QUALITY, quality])
  # Преобразование изображения обратно в numpy массив
  compressed_image_np = cv2.imdecode(compressed_image, cv2.IMREAD_COLOR)
  return compressed_image_np

def resize_image(img):
  n_width=720
  n_height=1280
  return cv2.resize(img, (n_width, n_height))

def preproc_image(image, image_proc_cfg):
  image = compress_and_process_image(image, **image_proc_cfg)
  return image

def preproc_image_from_file(image_filepath, image_proc_cfg):
  image = resize_image(read_image_from_file(image))
  image = preproc_image(image, image_proc_cfg)
  return image

def get_reader(reader_cfg):
  # docs - https://www.jaided.ai/easyocr/documentation/
  reader_default_cfg = {
    'lang_list': ['ru', 'en'],
    'gpu': True,
    'download_enabled': False,
    'model_storage_directory': './EasyOCR/model/',
  }
  reader_cfg = {**reader_default_cfg, **reader_cfg}
  reader = easyocr.Reader(**reader_cfg)
  return reader

def list_images_to_text(images, reader=None, reader_cfg={}):
  image_proc_cfg = {
    'width': 700,
    'quality': 0,
  }
  images = [
    preproc_image_from_file(image, image_proc_cfg) if isinstance(image, str) else preproc_image(image, image_proc_cfg)
    for image in images
  ]
  if reader is None:
    reader = get_reader(reader_cfg)
  results = reader.readtext_batched(
    images,
  )
  result = [
    ' '.join(r[1] for r in img_result)
    for img_result in results
  ]
  return result

def image_to_text(image, reader=None, reader_cfg={}):
  if isinstance(image, str): # check if image path is str/filepath
    image = read_image_from_file(image)
  if reader is None:
    reader = get_reader(reader_cfg)
  results = reader.readtext(image=image)
  result_text = ' '.join(r[1] for r in results)
  return result_text

if __name__ == '__main__':
  import sys
  from pprint import pprint
  # Single image
  '''
  img_filepath = sys.argv[1]
  print(f'{img_filepath=}')
  img_text = image_to_text(img_filepath)
  print(img_text)
  '''
  # Multiple images
  img_dir_filepath = sys.argv[1]
  print(f'{img_dir_filepath=}')
  import glob
  img_files = glob.glob(f'{img_dir_filepath}/*')
  img_text = list_images_to_text(img_files)
  pprint(dict(zip(img_files, img_text)))

