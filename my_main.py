import os
import hashlib
import requests
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from io import BytesIO
import html2text
from docx.shared import Inches
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
from htmldocx import HtmlToDocx

"""
Создаем директорию с названием новости
Создаем документ *.docx с названием новости
Скачиваем картинки из новости и помещаем в директорию названия новости
Скачиваем доп материалы к новости и сохраняем в директорию 'название новости/matetials'

"""

# Список URL для JSON данных
json_urls = [
    "https://academyopen.ru/api-7/news/903111",
    "https://academyopen.ru/api-7/news/903",

    # ...  другие URL-ы с JSON данными
]


def add_empty_line(doc):  # Пустая строка
    doc.add_paragraph("")


def html_to_plain_text(html):
    h = html2text.HTML2Text()
    h.ignore_links = True
    return h.handle(html)


# def add_text_block(doc, text, font_size, font_style=None, alignment=WD_PARAGRAPH_ALIGNMENT.LEFT,
#                    spacing_after=Pt(0)):
#     paragraph = doc.add_paragraph()
#     run = paragraph.add_run()
#
#     if font_style:
#         if "bold" in font_style:
#             run.bold = True
#         if "italic" in font_style:
#             run.italic = True
#
#     run.font.size = Pt(font_size)
#     run.text = text
#
#     paragraph.alignment = alignment
#     paragraph.paragraph_format.space_after = spacing_after
#     return paragraph

def add_text_block(doc, text, font_size, font_style=None, alignment=WD_PARAGRAPH_ALIGNMENT.LEFT,
                   spacing_after=Pt(0)):
    paragraph = doc.add_paragraph()
    run = paragraph.add_run()

    if font_style:
        if "bold" in font_style:
            run.bold = True
        if "italic" in font_style:
            run.italic = True

    run.font.size = Pt(font_size)
    run.text = text

    paragraph.alignment = alignment
    paragraph.paragraph_format.space_after = spacing_after
    return paragraph


# Для каждого URL получаем JSON данные и создаем документ
# for json_url in tqdm(json_urls, desc="Процесс JSON URLs"):
for json_url in json_urls:
    try:
        response = requests.get(json_url)
        response.raise_for_status()  # Проверка на успешный ответ (код 200)
        your_json = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных из URL: {json_url}")
        print(f"Ошибка: {e}")
        continue  # Прерываем итерацию и переходим к следующему URL

    # Создаем папку для сохранения документов, если её еще нет
    title = your_json["data"]["title"]
    title_for_folder = title.replace('/', '_').replace(':', '_')  # Удаляем недопустимые знаки
    folder_path = os.path.join(os.getcwd(), title_for_folder)
    os.makedirs(folder_path, exist_ok=True)
    # print(f"Создана директория: {folder_path}")

    # Путь к файлу .docx внутри папки
    docx_filename = os.path.join(folder_path, f"{title_for_folder}.docx")
    # print(f"Создан файл: {docx_filename}")

    # Создание документа
    doc = Document()
    # Создание объекта конвертера
    html_to_docx = HtmlToDocx()

    doc.styles['Normal'].font.name = 'Times New Roman'
    # Добавление таблицы для втавки значений Заголовок и Дискриптион
    table = doc.add_table(rows=2, cols=2)
    table.autofit = True

    # Добавление названия статьи
    add_text_block(doc, title, 14, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
    # print(f"Title: {title}")

    # Получение значения из поля "subtitle"
    subtitle = your_json["data"]["subtitle"]
    # print(f"Subtitle: {subtitle}")

    # Получение значения из поля "seoDescription"
    seo_description = your_json["data"]["rubric"]["seoDescription"]
    add_text_block(doc, seo_description, 12, alignment=WD_PARAGRAPH_ALIGNMENT.LEFT)
    # print(f"seoDescription: {seo_description}")

    add_text_block(doc, subtitle, 12, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)  # Подзаголовок
    add_empty_line(doc)  # Вызов функции для добавления пустой строки

    # Получение значения "materials"
    materials = your_json["data"]["materials"]
    # print(f"Доп материалы: {materials}")

    # Создание папки для дополнительных материалов
    materials_folder = os.path.join(folder_path, "materials")
    os.makedirs(materials_folder, exist_ok=True)

    # Скачивание дополнительных материалов (если есть)
    if materials:
        for material in materials:
            material_name = material["name"]
            material_url = material["file"]
            material_extension = material_url.split(".")[-1]
            material_filename = f"{material_name}.{material_extension}"
            material_path = os.path.join(materials_folder, material_filename)
            try:
                material_response = requests.get(material_url)
                material_response.raise_for_status()  # Проверка на успешный ответ (код 200)
                with open(material_path, "wb") as material_file:
                    material_file.write(material_response.content)
                print(f"Дополнительный материал скачан: {material_path}")
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при скачивании материала {material_name}: {e}")
    else:
        print("Нет дополнительных материалов.")


    # total_text_blocks = len(your_json["data"]["blocks"])
    # text_bar = tqdm(total=total_text_blocks, desc='Вставка текста')
    # text_bar = tqdm(total=total_text_blocks, desc='Вставка текста', mininterval=0.01)

    # Добавление текстовых блоков из "blocks"
    for block in tqdm(your_json["data"]["blocks"], desc="Processing blocks"):
        # for block in your_json["data"]["blocks"]:
        block_type = block["blockType"]
        if block_type == 1:  # Основной текст
            text = block.get("text")
            if text:
                # Преобразование HTML в DOCX
                html_to_docx.add_html_to_document(text, doc)
                # text_bar.update(1)
                add_empty_line(doc)  # Вставляем пустую строку

        elif block_type == 10:  # Заголовок
            text = block.get("text")
            if text:
                add_text_block(doc, text, 16, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
                add_empty_line(doc)
        elif block_type == 11:  # Список
            elem_list = block.get("elemList")
            if elem_list and elem_list["elemType"] == 2:
                elems = elem_list["elems"]
                if elems:
                    for elem in elems:
                        add_text_block(doc, "- " + elem, 10, alignment=WD_PARAGRAPH_ALIGNMENT.LEFT)
                    add_empty_line(doc)
        elif block["blockType"] == 5 and "carousel" in block:  # Картинки
            carousel_images = block["carousel"]
            # Обработка скачивания изображений
            for index, carousel_item in enumerate(carousel_images):
                image_url = carousel_item["image"]
                image_response = requests.get(image_url)
                image_extension = image_url.split(".")[-1]
                image_hash = hashlib.md5(image_response.content).hexdigest()
                image_filename = f"carousel_{index + 1}.{image_extension}"  # Изменил имя для изображений
                image_path = os.path.join(folder_path, image_filename)
                try:
                    image_response.raise_for_status()  # Проверка на успешный ответ (код 200)
                    with open(image_path, "wb") as image_file:
                        image_file.write(image_response.content)
                    print(f"Изображение из блока 'blockType:5''carousel' сохранено: {image_path}")
                except requests.exceptions.RequestException as e:
                    print(f"Ошибка при скачивании изображения {image_url}: {e}")
                # Добавление подписи к изображению
                sign = carousel_item.get("sign")
                if sign is not None:
                    add_empty_line(doc)
                    # Вставка изображения в docx
                    doc.add_picture(image_path, width=Inches(6.0))  # Изменение размеров картинки
                    if sign:
                        # Добавление комментария, если он есть
                        # add_text_block(doc, "Комментарий:", 12, WD_PARAGRAPH_ALIGNMENT.LEFT)
                        add_text_block(doc, sign, 10, font_style='italic', alignment=WD_PARAGRAPH_ALIGNMENT.LEFT)
                    add_empty_line(doc)
                else:
                    # Вставка изображения в docx без комментария
                    doc.add_picture(image_path, width=Inches(6.0))  # Изменение размеров картинки
                    add_empty_line(doc)
        # text_bar.close()

    # Сохранение документа названием статьи в папку с названием статьи
    doc.save(docx_filename)
    print(
        f"Документ сохранен: {docx_filename}\n------------------------------------------------------------------------------")
