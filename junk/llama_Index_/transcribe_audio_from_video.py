
import os
import whisper

# Загрузка модели Whisper
model_whisper = whisper.load_model("large")

def transcribe(path):
    """
    Транскрибировать аудиофайл в текст с использованием модели Whisper.

    Параметры:
    path (str): Путь к аудиофайлу.

    Возвращает:
    str: Транскрибированный текст.
    """
    print("Транскрибирование...", path)
    result = model_whisper.transcribe(path)
    return result["text"]

def process_all_audio_files(directory, output_folder):
    """
    Обработать все mp4 файлы в директории, преобразовать их в текст,
    сохранить текст в файлы и, при необходимости, удалить исходные аудиофайлы.

    Параметры:
    directory (str): Путь к директории с аудиофайлами.
    output_folder (str): Путь к директории для сохранения текстовых файлов.
    """
    # Убедимся, что входная и выходная директории существуют
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Создана директория: {directory}")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Создана выходная папка: {output_folder}")
        
    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            audio_path = os.path.join(directory, filename)
            print(f"Обработка файла: {audio_path}")
            text_data = transcribe(audio_path)

            # Определяем путь для текстового файла
            text_filename = os.path.splitext(filename)[0] + ".txt"
            text_file_path = os.path.join(output_folder, text_filename)

            # Сохраняем текстовые данные в файл
            with open(text_file_path, "w", encoding="utf-8") as file:
                file.write(text_data)

            print(f"Текстовые данные сохранены в файл: {text_file_path}")

            # Опционально удалить аудиофайл
            # os.remove(audio_path)
            # print(f"Аудиофайл удален: {audio_path}")

# Пример использования
if __name__ == "__main__":
    directory_path = "./video"
    output_folder = "./mixed_data"
    process_all_audio_files(directory_path, output_folder)
