import os
import hashlib
import requests
from docx import Document
from docx.opc.oxml import qn
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from io import BytesIO
import html2text
from docx.shared import Inches
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
from htmldocx import HtmlToDocx
from docx.shared import Pt
from docx.oxml.ns import qn
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
import html2text

"""
Создаем директорию с названием новости
Создаем документ *.docx с названием новости
Скачиваем картинки из новости и помещаем в директорию названия новости
Скачиваем доп материалы к новости и сохраняем в директорию 'название новости/matetials'

"""

# Список URL для JSON данных
json_urls = [

    "https://academyopen.ru/api-7/news/900",

    # ...  другие URL-ы с JSON данными
]


def add_empty_line(doc):  # Пустая строка
    doc.add_paragraph("")


def html_to_plain_text(html):
    h = html2text.HTML2Text()
    h.ignore_links = True
    return h.handle(html)


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


def clean_filename(filename):
    invalid_chars = r'\/:*?"<>|'  # Здесь перечислены недопустимые символы
    cleaned_filename = ''.join(c for c in filename if c not in invalid_chars)
    return cleaned_filename


# Для каждого URL получаем JSON данные и создаем документ
# for json_url in tqdm(json_urls, desc="Процесс JSON URLs"):
# Статус-бар для JSON-файлов
total_json_urls = len(json_urls)
json_bar = tqdm(total=total_json_urls, desc='Процесс JSON URLs')
for json_url in json_urls:
    try:
        response = requests.get(json_url)
        response.raise_for_status()  # Проверка на успешный ответ (код 200)
        your_json = response.json()
        json_bar.update(1)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных из URL: {json_url}")
        print(f"Ошибка: {e}")
        continue  # Прерываем итерацию и переходим к следующему URL

    material_folder_name = "Материалы"

    # Создаем папку для сохранения документов, если её еще нет
    title = your_json["data"]["title"]
    title_for_folder = clean_filename(title)  # Используем функцию для обработки имени
    folder_path = os.path.join(os.getcwd(), material_folder_name, title_for_folder)

    os.makedirs(folder_path, exist_ok=True)
    print(f"Создана директория: {folder_path}")

    # Путь к файлу .docx внутри папки
    docx_filename = os.path.join(folder_path, f"{title_for_folder}.docx")
    print(f"Создан файл: {docx_filename}")

    # Создание документа
    doc = Document()
    # Создание объекта конвертера
    html_to_docx = HtmlToDocx()

    doc.styles['Normal'].font.name = 'Times New Roman'
    # Добавление таблицы для вставки значений Заголовок и Дискриптион
    table = doc.add_table(rows=3, cols=2)
    table.autofit = True
    # Установка стиля границ таблицы для тонких линий
    table.style = 'Table Grid'
    # Вставка заголовков в первый столбец
    table.cell(0, 0).text = "Title"
    table.cell(1, 0).text = "Description"
    print("Добавлена таблица")

    # Получение значения из поля "id"
    id_ = your_json["data"]["id"]
    add_text_block(doc, str(id_), 10, alignment=WD_PARAGRAPH_ALIGNMENT.LEFT)  # Добавление названия ID статьи
    print(f"ID статьи: {id_}")

    # Добавление названия статьи
    add_text_block(doc, title, 14, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
    print(f"Title стать: {title}")

    # Получение значения из поля "subtitle"
    subtitle = your_json["data"]["subtitle"]
    print(f"Subtitle статьи: {subtitle}")

    # Получение значения из поля "seoDescription"
    seo_description = your_json["data"]["rubric"]["seoDescription"]
    # add_text_block(doc, seo_description, 12, alignment=WD_PARAGRAPH_ALIGNMENT.LEFT)
    print(f"seoDescription: {seo_description}")

    add_text_block(doc, subtitle, 12, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)  # Подзаголовок
    add_empty_line(doc)  # Вызов функции для добавления пустой строки

    # Получение значения "materials"
    materials = your_json["data"]["materials"]
    print(f"Доп материалы: {materials}")

    # Вставка значений title и seo_description во второй столбец
    table.cell(0, 1).text = title
    table.cell(1, 1).text = seo_description

    table.cell(2, 0).text = "Дополнительные материалы"
    # table.cell(2, 1).text = materials_info

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
                materials_info = material_name
                table.cell(2, 1).text = materials_info  # Добавление в таблицу инфу о доп материале
            except requests.exceptions.RequestException as e:

                error_message = f"Ошибка при скачивании материала {material_name}: {e}"
                colored_error_message = f"\033[91m{error_message}\033[0m"
                print(colored_error_message)
                materials_info = f"Ошибка скачивания материала: {material_name}"

                # Создаем объект run для стилизации текста
                run = table.cell(2, 1).paragraphs[0].add_run(materials_info)

                # Применяем стили шрифта (красный цвет)
                font = run.font
                font.color.rgb = RGBColor(255, 0, 0)  # Красный цвет
    else:
        print("Нет дополнительных материалов.")
        materials_info = "Нет дополнительных материалов"  # Добавление информации в таблицу о доп материалах
        table.cell(2, 1).text = materials_info

    # total_text_blocks = len(your_json["data"]["blocks"])
    # text_bar = tqdm(total=total_text_blocks, desc='Вставка текста')
    # text_bar = tqdm(total=total_text_blocks, desc='Вставка текста', mininterval=0.01)

    # Добавление текстовых блоков из "blocks"
    # for block in tqdm(your_json["data"]["blocks"], desc="Processing blocks"):
    for block in your_json["data"]["blocks"]:
        block_type = block["blockType"]
        if block_type == 1:  # Основной текст
            text = block.get("text")

            if text:
                # Преобразование HTML в DOCX
                html_to_docx.add_html_to_document(text, doc)
                print(f"Добавлен: Основной текст")
                # text_bar.update(1)
                # add_empty_line(doc)  # Вставляем пустую строку

        elif block_type == 10:  # Заголовок
            text = block.get("text")
            if text:
                # add_text_block(doc, text, 16, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
                html_to_docx.add_html_to_document(text, doc)
                print(f"Добавлен: Заголовок")
                # add_empty_line(doc)

        # if block["blockType"] == 11:  # Список
        #     list_items_html = block["elemList"]["elems"]
        #     for item_html in list_items_html:
        #         # Создаем параграф для элемента списка
        #         paragraph = doc.add_paragraph(style="List Bullet")
        #
        #         # Добавляем знак "-" перед тегом <strong>
        #         # run = paragraph.add_run("- ")
        #         # run.bold = False
        #
        #         # Преобразуем HTML в текст и добавляем его в параграф
        #         soup = BeautifulSoup(item_html, "html.parser")
        #         text = soup.get_text()
        #         paragraph.add_run(text)
        #
        #         # Устанавливаем стиль для текста в параграфе
        #         for run in paragraph.runs:
        #             run.font.size = Pt(12)
        #             run.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

        elif block["blockType"] == 11:
            # Извлекаем элементы списка
            list_items_html = block["elemList"]["elems"]
            for item in list_items_html:
                html_to_docx.add_html_to_document(item, doc)
                print(f"Добавлен: Элемент списка")

        elif block_type == 2:  # Комментарий пользователя сервиса
            text = block.get("text")
            author = block.get("author")
            if text:
                # add_text_block(doc, text, 11, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
                html_to_docx.add_html_to_document(text, doc)
                html_to_docx.add_html_to_document(author, doc)
                print(f"Добавлен: Текст комментария пользователя сервиса")

            if author:
                # add_text_block(doc, text, 11, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)

                html_to_docx.add_html_to_document(author, doc)
                print(f"Добавлен: Автор комментария пользователя сервиса")

        # elif block_type == 2:  # Автор комментария пользователя сервиса
        #     author = block.get("author")
        #     if author:
        #         # Преобразование HTML в DOCX
        #         # add_text_block(doc, author, 11, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
        #         html_to_docx.add_html_to_document(author, doc)
        #         print(f"Добавлен: Автор комментария пользователя сервиса")

        elif block["blockType"] == 5 and "carousel" in block:  # Картинки
            carousel_images = block["carousel"]
            # total_images = len(carousel_images)
            #
            # # Создание статус-бара для скачивания изображений
            # progress_bar = tqdm(total=total_images, desc="Скачивание изображений")

            for index, carousel_item in enumerate(carousel_images):

                image_url = carousel_item["image"]
                image_response = requests.get(image_url)

                image_extension = image_url.split(".")[-1]
                image_hash = hashlib.md5(image_response.content).hexdigest()
                image_filename = f"carousel_{image_hash}.{image_extension}"
                image_path = os.path.join(folder_path, image_filename)
                with open(image_path, "wb") as image_file:
                    image_file.write(image_response.content)
                try:
                    image_response.raise_for_status()  # Проверка на успешный ответ (код 200)
                    with open(image_path, "wb") as image_file:
                        image_file.write(image_response.content)
                    print(f"Изображение из блока 'blockType:5''carousel' сохранено: {image_path}")

                except requests.exceptions.RequestException as e:
                    print(f"Ошибка при скачивании изображения {image_url}: {e}")
                    error_message = f"Ошибка при скачивании изображения {image_url}: {e}"
                    colored_error_message = f"\033[91m{error_message}\033[0m"
                    print(colored_error_message)

                # Добавление подписи к изображению
                sign = carousel_item.get("sign")
                if sign is not None:
                    add_empty_line(doc)
                    # Вставка изображения в docx
                    doc.add_picture(image_path, width=Inches(6.0))  # Изменение размеров картинки
                    print(f"Добавлен: Изображение")
                    if sign:
                        # Добавление комментария, если он есть
                        # add_text_block(doc, "Комментарий:", 12, WD_PARAGRAPH_ALIGNMENT.LEFT)
                        add_text_block(doc, sign, 10, font_style='italic', alignment=WD_PARAGRAPH_ALIGNMENT.LEFT)
                        print(f"Добавлен: Комментарий к изображению")
                    add_empty_line(doc)
                else:
                    # Вставка изображения в docx без комментария
                    doc.add_picture(image_path, width=Inches(6.0))  # Изменение размеров картинки
                    # add_empty_line(doc)
                    print(f"Добавлен: Изображение без комментария")

    # Сохранение документа названием статьи в папку с названием статьи
    doc.save(docx_filename)
    print(
        f"Документ сохранен: {docx_filename}\n------------------------------------------------------------------------------")
    json_bar.close()
