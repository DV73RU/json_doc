import os
import requests
import re
from read_list_json import read_links_from_file
import logging

"""
Создаем директорию с названием новости ("data": "title":)
Скачиваем видео из новости и помещаем в директорию названия новости ("blocks": "link":)
Переименовываем видео в название подписи под видео из новости ("blocks": "title":)


"""
file_path = "list_json_business.txt"
# Получаем список ссылок из файла
links = read_links_from_file(file_path)
# Логирование ошибок
logging.basicConfig(filename='err_log.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='utf-8')


# Список URL для JSON данных
json_urls = links

"""

Скачивание видео контента из JSON ответа.

"""


# Загрузка списка URL из файла
with open(file_path, "r") as file:
    urls = file.readlines()

# Удаляем лишние пробелы и символы перевода строки из URL
urls = [url.strip() for url in urls]


# Функция для очистки строки от недопустимых символов
def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '', filename)


# Функция для извлечения расширения файла из URL
def get_file_extension(url):
    # Используем регулярное выражение для поиска расширения в URL
    match = re.search(r'\.(\w+)$', url)
    if match:
        return match.group(1)
    else:
        return None


# Перебираем URL и отправляем GET запрос к каждому из них
for url in urls:
    try:
        # Отправляем GET запрос
        response = requests.get(url, headers=headers)

        # Проверяем, успешно ли получен ответ
        if response.status_code == 200:
            # Загружаем JSON данные из ответа
            data = response.json()
            print(f"=={url} -  {response.status_code}")

            # Извлекаем значение "name" из JSON-данных
            folder_name = data.get("data", {}).get("name")

            if folder_name:
                # Очищаем имя папки от недопустимых символов
                folder_name = clean_filename(folder_name)

                # Создаем папку с названием из "name", если она не существует
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                    print(f"Создана директория: {folder_name}")

                # Извлекаем список "lessons" из JSON-данных
                lessons = data.get("data", {}).get("lessons", [])

                # Перебираем уроки в списке "lessons"
                for lesson in lessons:
                    # Извлекаем информацию о файле из урока
                    material_name = lesson.get("title")
                    m3u8_url = lesson.get("video")

                    if material_name and m3u8_url:
                        # Очищаем имя файла от недопустимых символов
                        material_name = clean_filename(material_name)

                        # Преобразуем M3U8-ссылку в MP4-ссылку
                        mp4_url = m3u8_url.replace('/_HLS_/', '/').replace('/playlist.m3u8', '.mp4')
                        print(f"Ссылка скачивания файла: {mp4_url}")
                        # Определяем путь для сохранения файла внутри созданной папки
                        file_path = os.path.join(folder_name, material_name + '.mp4')

                        # Загружаем файл и проверяем код ответа
                        response = requests.get(mp4_url)

                        if response.status_code == 200:
                            with open(file_path, "wb") as file:
                                file.write(response.content)
                                print(f"Ссылка на файл '{material_name + '.mp4'}' Код статуса: {response.status_code}")
                        else:
                            print(
                                f"Ошибка при скачивании файла '{material_name + '.mp4'}'. Код статуса: {response.status_code}")

                        # Загружаем и сохраняем файл
                        response = requests.get(mp4_url)
                        with open(file_path, "wb") as file:
                            file.write(response.content)

                        print(f"Файл '{material_name + '.mp4'}' сохранен в папке '{folder_name}'")
                    else:
                        print("Недостаточно данных для сохранения файла.")

                    # Извлекаем список "materials" из JSON-данных
                    # materials = data.get("data", {}).get("materials", [])

                    # Проверяем наличие "materials" внутри урока
                    materials = lesson.get("materials", [])

                    # Перебираем материалы в списке "materials"
                    for material in materials:
                        # Извлекаем информацию о файле из материала
                        material_name = material.get("name")
                        material_url = material.get("file")

                        if material_name and material_url:
                            # Очищаем имя файла от недопустимых символов
                            material_name = clean_filename(material_name)

                            # Определяем расширение файла из URL
                            file_extension = get_file_extension(material_url)

                            # Если расширение найдено, добавляем его к имени файла
                            if file_extension:
                                material_name_with_extension = material_name + '.' + file_extension
                            else:
                                material_name_with_extension = material_name

                            # Определяем путь для сохранения файла внутри созданной папки
                            material_file_path = os.path.join(folder_name, material_name_with_extension)

                            # Загружаем и сохраняем файл
                            response = requests.get(material_url)

                            if response.status_code == 200:
                                with open(material_file_path, "wb") as file:
                                    file.write(response.content)
                                print(f"Файл '{material_name_with_extension}' сохранен в папке '{folder_name}'")
                            else:
                                print(
                                    f"Ошибка при скачивании файла '{material_name_with_extension}'. Код статуса: {response.status_code}")
            else:
                print("Название папки ('name') не найдено в JSON-данных.")
        else:
            print(f"Ошибка при получении JSON {url} данных. Код статуса: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")
    except ValueError as e:
        print(f"Произошла ошибка при обработке JSON данных: {e}")