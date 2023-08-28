"""
Парсим блоки json

узнать в какой новости присутствуют интересующие  блоки

"""
import openpyxl
import requests
from tqdm import tqdm  # Импорт библиотеки tqdm
from read_list_json import read_links_from_file

# Список ссылок

file_path = "links_with_numbers.txt"
# Получаем список ссылок из файла
links = read_links_from_file(file_path)

# Список URL для JSON данных
json_urls = links

block_type_values = []

# Создаем новый Excel файл
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Block Types"

# Записываем заголовки
ws.append(["Дата", "Название статьи", "Ссылка"])

# Проход по каждой ссылке
for link in links:
    # Отправка GET-запроса к ссылке и получение JSON-данных
    response = requests.get(link)
    if response.status_code == 200:
        json_data = response.json()

        # Получение всех значений blockType для блоков в JSON-данных
        for block in json_data["data"]["blocks"]:
            block_type = block["blockType"]
            if block_type is not None:
                block_type_values.append(block_type)

        # Удаление дублирующихся значений и преобразование в список
        unique_block_type_values = list(set(block_type_values))

        # Вывод ссылки и списка уникальных значений blockType, если он не пустой
        if unique_block_type_values:
            print(f"Link: {link} : Пресутсвуют блоки: {unique_block_type_values}")
            # print(f"Пресутсвуют блоки: {unique_block_type_values}")
    else:
        print(f"Link: {link} недоступен")

# Сохраняем файл
excel_file_path = "block_types.xlsx"
wb.save(excel_file_path)
print(f"Данные успешно записаны в Excel файл: {excel_file_path}")