from urllib.request import urlretrieve
from zipfile import ZipFile
from pathlib import Path
import os

# from https://github.com/JaidedAI/EasyOCR/blob/master/easyocr/config.py
#recognition_models['gen2']['cyrillic_g2']

# self.detect_network = craft
#self.detection_models[self.detect_network]['url']

MODULE_PATH = './EasyOCR/'
model_storage_directory = os.path.join(MODULE_PATH, 'model')
print(f'{model_storage_directory=}')
Path(model_storage_directory).mkdir(parents=True, exist_ok=True)

def printProgressBar(prefix='', suffix='', decimals=1, length=100, fill='█'):
  """
  Call in a loop to create terminal progress bar
  @params:
      prefix      - Optional  : prefix string (Str)
      suffix      - Optional  : suffix string (Str)
      decimals    - Optional  : positive number of decimals in percent complete (Int)
      length      - Optional  : character length of bar (Int)
      fill        - Optional  : bar fill character (Str)
      printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
  """
  def progress_hook(count, blockSize, totalSize):
      progress = count * blockSize / totalSize
      percent = ("{0:." + str(decimals) + "f}").format(progress * 100)
      filledLength = int(length * progress)
      bar = fill * filledLength + '-' * (length - filledLength)
      print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='')
  return progress_hook

def download_and_unzip(url, filename, model_storage_directory):
  print(f'Downloading {filename}')
  zip_path = os.path.join(model_storage_directory, 'temp.zip')
  urlretrieve(url, zip_path, reporthook=printProgressBar(prefix='Progress:', suffix='Complete', length=50))
  print()
  with ZipFile(zip_path, 'r') as zipObj:
    zipObj.extract(filename, model_storage_directory)
  os.remove(zip_path)

def download_easyocr_model():
  detection_model_craf = {
    'filename': 'craft_mlt_25k.pth',
    'url': 'https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/craft_mlt_25k.zip',
    'md5sum': '2f8227d2def4037cdb3b34389dcf9ec1',
  }
  recognition_model_gen2_cyrillic_g2 = {
    'filename': 'cyrillic_g2.pth',
    'model_script': 'cyrillic',
    'url': 'https://github.com/JaidedAI/EasyOCR/releases/download/v1.6.1/cyrillic_g2.zip',
    'md5sum': '19f85f43d9128a89ac21b8d6a06973fe',
    'symbols': '0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ €₽',
    'characters': '0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ €₽ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяЂђЃѓЄєІіЇїЈјЉљЊњЋћЌќЎўЏџҐґҒғҚқҮүҲҳҶҷӀӏӢӣӨөӮӯ',
  } 
  download_and_unzip(
    url=detection_model_craf['url'],
    filename=detection_model_craf['filename'],
    model_storage_directory=model_storage_directory,
  )
  download_and_unzip(
    url=recognition_model_gen2_cyrillic_g2['url'],
    filename=recognition_model_gen2_cyrillic_g2['filename'],
    model_storage_directory=model_storage_directory,
  )

if __name__ == '__main__':
  download_easyocr_model()
