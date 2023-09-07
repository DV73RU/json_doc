"""
Проверяем ответ 200 у URL из списка links_with_numbers.txt.
Сохраняем список с ответом 200 в файл list_json_business.txt
Ищём URL из файла links_with_numbers_business.txt c JSON ответом блоком "slug": "business-cases"
Сохраняем список найденных url в список links_business_cases.txt,
"""

# Импортируем библиотеки
import requests
import os
import re
from tqdm import tqdm  # Импортируем tqdm


def clean_folder_name(name):
    # Удалить все недопустимые символы для имен папок
    cleaned_name = re.sub(r'[\/:*?"<>|]', '', name)
    return cleaned_name


# Определяем функцию для преобразования и скачивания видео
# def download_and_rename_video(url, output_folder):
#     response = requests.get(url, stream=True)
#     if response.status_code == 200:
#         content_type = response.headers.get('content-type')
#         if 'video' in content_type:
#             title = url.split('/')[-2]  # Используем часть URL в качестве имени файла
#             title += ".mp4"
#             file_path = os.path.join(output_folder, title)
#
#             # Используем tqdm для отслеживания прогресса скачивания
#             total_size = int(response.headers.get('content-length', 0))
#             with open(file_path, 'wb') as video_file, tqdm(
#                     desc=title,  # Описание прогресса (имя файла)
#                     total=total_size,  # Общий размер файла для отслеживания
#                     unit='B',  # Единицы измерения (байты)
#                     unit_scale=True,  # Автоматический выбор единиц (KB, MB, GB)
#                     unit_divisor=1024  # Делитель для автоматического выбора единиц
#             ) as progress:
#                 for data in response.iter_content(chunk_size=1024):
#                     video_file.write(data)
#                     progress.update(len(data))
#             return True
#     return False

import requests
import os
from tqdm import tqdm

# Определяем функцию для преобразования и скачивания видео
def download_and_rename_video(url, output_folder):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        content_type = response.headers.get('content-type')
        if 'video' in content_type:
            # Получаем имя файла из URL
            file_name = url.split('/')[-1]
            # Удаляем '/playlist.m3u8' и добавляем '.mp4'
            file_name = file_name.replace('/playlist.m3u8', '')
            file_path = os.path.join(output_folder, file_name)

            total_size = int(response.headers.get('content-length', 0))
            with open(file_path, 'wb') as video_file:
                for data in response.iter_content(chunk_size=1024):
                    video_file.write(data)

            return True
    return False

# Открываем файл с исходными URL и читаем его содержимое
with open('list_json_business.txt', 'r') as file:
    urls = file.readlines()

# Создаем пустой список для хранения URL с блоком "slug": "business-cases"
valid_urls = []

# Проходим по каждому URL из списка
# Создаем статус-бар с помощью tqdm
with tqdm(total=len(urls), unit=' URL') as pbar:
    for url in urls:
        # Убираем лишние пробелы и переносы строк
        url = url.strip()

        # Отправляем GET-запрос к URL
        response = requests.get(url)

        # Проверяем, получен ли ответ со статусом 200
        if response.status_code == 200:
            # Извлекаем JSON-данные из ответа
            json_data = response.json()
            # Обновляем статус-бар
            pbar.update(1)

            # Проверяем, содержит ли JSON-данные блок "data" и внутри него блок "rubric" с "slug": "business-cases"
            if "data" in json_data and "rubric" in json_data["data"] and "slug" in json_data["data"]["rubric"] and \
                    json_data["data"]["rubric"]["slug"] == "business-cases":
                valid_urls.append(url)

# Создаем файл list_json_business.txt и записываем в него действительные URL
with open('list_json_business.txt', 'w') as file:
    for valid_url in valid_urls:
        file.write(valid_url + '\n')

# Выводим URL, в которых найден блок "slug": "business-cases"
print(f"Найдено {len(valid_urls)} URL с блоком 'slug': 'business-cases':")
for matching_url in valid_urls:
    print(matching_url)

# Открываем файл с URL, где есть блок "slug": "business-cases"
with open('list_json_business.txt', 'r') as file:
    urls = file.readlines()

# Создаем пустой список для хранения URL с видео
video_urls = []

# Создаем папку для сохранения видео
output_folder = 'videos'
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Проходим по каждому URL из списка
for url in urls:
    url = url.strip()
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()

        # Проверяем, содержит ли JSON-данные блок "slug": "business-cases"
        if "data" in json_data and "rubric" in json_data["data"] and "slug" in json_data["data"]["rubric"] and \
                json_data["data"]["rubric"]["slug"] == "business-cases":
            # Найден URL с блоком "slug": "business-cases", добавляем его в список
            video_urls.append(url)

# Проходим по найденным URL с блоком "slug": "business-cases"
for url in video_urls:
    response = requests.get(url)
    json_data = response.json()

    # Ищем блоки с "blockType": 3 и обрабатываем их
    if "data" in json_data and "blocks" in json_data["data"]:
        for block in json_data["data"]["blocks"]:
            if "blockType" in block and block["blockType"] == 3:
                link = block.get("link")
                if link:
                    # Преобразуем ссылку на видео
                    link = link.replace('/_HLS_/', '/').replace('/playlist.m3u8', '.mp4')

                    # Определяем имя папки из блока "data": "title"
                    # folder_name = json_data["data"]["title"]
                    folder_name = clean_folder_name(json_data["data"]["title"])

                    # Создаем папку для сохранения видео, если её нет
                    output_folder = os.path.join('videos', folder_name)
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)

                    # Скачиваем и сохраняем видео с нужным именем и расширением
                    success = download_and_rename_video(link, output_folder)

                    if success:
                        print(f"Видео успешно скачано: {link}")

# Выводим список URL с видео
print(f"Найдено {len(video_urls)} URL с видео:")
for video_url in video_urls:
    print(video_url)
