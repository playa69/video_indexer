import os
import re
from tqdm import tqdm
from moviepy.editor import VideoFileClip
from PIL import Image
from  llama_index.core import SimpleDirectoryReader
from llama_index.multi_modal_llms.ollama import OllamaMultiModal  


def process_all_videos_in_folder(input_folder, output_folder):
    """
    Обработать все файлы MP4 в указанной папке и преобразовать их в центральный кадр.

    Параметры:
    input_folder (str): Путь к папке с видео файлами.
    output_folder (str): Путь к папке для сохранения изображений.
    """
    # Проверяем, существует ли выходная папка, если нет - создаем ее
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Проходимся по всем файлам в указанной папке
    for filename in os.listdir(input_folder):
        if filename.endswith(".mp4"):
            video_path = os.path.join(input_folder, filename)
            extract_middle_frame(video_path, output_folder)
            print(f'Обработано видео: {filename}')




def extract_middle_frame(video_path, output_folder):
    """
    Извлечь центральный кадр из видео и сохранить его в указанной папке.

    Параметры:
    video_path (str): Путь к видео файлу.
    output_folder (str): Путь к папке для сохранения изображений.
    """
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(output_folder, f"{base_name}.png")
    
    clip = VideoFileClip(video_path)
    middle_frame_time = clip.duration / 2
    
    # Извлекаем и сохраняем центральный кадр
    frame = clip.get_frame(middle_frame_time)
    frame_image = Image.fromarray(frame)
    frame_image.save(output_path)



def process_documents(input_folder, output_folder, model_name="llava:7b", request_timeout=512.0, temperature=0.7):
    """
    Обрабатывает документы, генерируя хэштеги для изображений и сохраняя результаты в текстовые файлы.

    Аргументы:
        input_folder (str): Путь к папке с исходными документами.
        output_folder (str): Путь к папке, куда будут сохраняться текстовые файлы.
        model_name (str): Имя модели для использования. По умолчанию "llava:7b".
        request_timeout (float): Таймаут запроса к модели в секундах. По умолчанию 512.0.
        temperature (float): Температура для генерации текста моделью. По умолчанию 0.7.
    """
    # Загружаем документы из указанной папки
    documents = SimpleDirectoryReader(input_folder).load_data()
    
    # Инициализируем мультимодальную модель
    mm_model = OllamaMultiModal(model=model_name, request_timeout=request_timeout, temperature=temperature)
    
    # Проверяем наличие выходной папки и создаем ее, если она отсутствует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Обрабатываем каждый документ
    for doc in tqdm(documents):
        # Запрашиваем у модели описание изображения в виде хэштегов
        req = mm_model.complete(
            'describe this image exclusively with hashtags and give an answer only with them', 
            image_documents=[doc]
        )
        hashtags_re = re.findall(r'#\w+', req.text)
        hashtags_re = ' '.join(hashtags_re)
        
        # Создаем имя файла на основе имени изображения, заменяя расширение png на txt
        filename = doc.metadata['file_name'].replace('png', 'txt')
        file_path = os.path.join(output_folder, filename)

        # Проверяем, существует ли файл
        if os.path.exists(file_path):
            # Читаем существующее содержимое файла
            with open(file_path, 'r', encoding='utf-8') as file:
                existing_content = file.read()

            # Добавляем новое описание в начало существующего содержимого
            new_content = hashtags_re + '\n' + existing_content

            # Записываем обновленное содержимое обратно в файл
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
        else:
            # Выводим предупреждение, если файл не найден
            print(f"Файл {file_path} не найден.")

def main():
    """
    Основная функция, которая сначала обрабатывает видео для извлечения центральных кадров,
    а затем генерирует хэштеги для извлеченных изображений.
    """
    video_input_folder = "video_"
    image_output_folder = "one_frame_from_video"
    txt_output_folder = "txt_data"

    # Обработка видео для извлечения центральных кадров
    process_all_videos_in_folder(video_input_folder, image_output_folder)

    # Генерация хэштегов для изображений и сохранение их в текстовые файлы
    process_documents(image_output_folder, txt_output_folder)

if __name__ == "__main__":
    main()
