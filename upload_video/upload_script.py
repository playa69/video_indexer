"""
def process_input_line(input_line):
    parts = input_line.split("\n")
    result = []

    for part in parts:
        if "https://" in part:
            url, *description = part.split(',', 1)
            url = url.strip()
            if description:
                description = description[0].strip().strip('"')
                result.append(f'("{url}", "{description}"),')
            else:
                result.append(f'("{url}"),')

    return result


def read_from_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        return file.read()


def write_to_file(output_file, processed_lines):
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in processed_lines:
            file.write(line + '\n')


# Указываем входной и выходной файлы
input_file = 'input.txt'
output_file = 'output.txt'

# Считываем данные из файла
input_line = read_from_file(input_file)

# Обрабатываем данные
processed_lines = process_input_line(input_line)

# Записываем результат в файл
write_to_file(output_file, processed_lines)

print(f'Обработка завершена. Результаты записаны в {output_file}') """
import requests


def read_from_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        pairs = []
        for line in file:
            parts = line.strip().split(',')
            url = parts[0].strip() if len(parts) > 0 else ''
            description = parts[1].strip() if len(parts) > 1 else ''
            pairs.append((url, description))
        return pairs

""" 
def read_from_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        return [tuple(line.strip().split(', ')) for line in file] """


def send_videos_with_descriptions(video_description_pairs):
    base_url = "http://176.123.161.67/api/add?url="
    for video_url, description in video_description_pairs:
        full_url = f"{base_url}{video_url}&description={description}"
        try:
            response = requests.get(full_url)
            if response.status_code == 200:
                print(f"Успешно добавлено: {video_url}")
            else:
                print(f"Не удалось добавить: {video_url}, статус-код: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при добавлении {video_url}: {e}")


input_file = 'input.txt'
output_file = 'output.txt'
read_from_file(output_file)

# Список видео URL и описаний

# Считываем данные из файла
video_description_pairs = read_from_file(output_file)

send_videos_with_descriptions(video_description_pairs)
