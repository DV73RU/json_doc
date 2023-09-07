"""
Парсим блоки json

узнать в какой новости присутствуют интересующие  блоки

"""
import openpyxl
import requests
from tqdm import tqdm  # Импорт библиотеки tqdm
from read_list_json import read_links_from_file

# Список ссылок

file_path = "list_json3.txt"
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
    response = requests.get(link)
    if response.status_code == 200:
        json_data = response.json()
        print(f"Link: {link} : OK")

        date = json_data["data"]["date"]
        article_title = json_data["data"]["title"]
        
        date_clear = date.split("T")[0]  # Отделяем от даты лишнее
        link_real = link.replace("api-7/news/", "journal/")
        ws.append([date_clear, article_title, link_real])
    else:
        print(f"Link: {link} : отсутствует либо недоступна")

# Изменение ширины столбца для названия статьи (например, до 40)
ws.column_dimensions["A"].width = 20  # "A" - второй столбец, "40" - новая ширина
ws.column_dimensions["B"].width = 60  # "B" - второй столбец, "40" - новая ширина
ws.column_dimensions["C"].width = 100  # "B" - второй столбец, "40" - новая ширина

# Сохраняем файл
excel_file_path = "block_types.xlsx"
wb.save(excel_file_path)
print(f"Данные успешно записаны в Excel файл: {excel_file_path}")
