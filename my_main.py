import os
import hashlib
import requests
from docx import Document
from docx.shared import Pt, RGBColor
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
    "https://academyopen.ru/api-7/news/903",
    "https://academyopen.ru/api-7/news/900",
    "https://academyopen.ru/api-7/news/902",
    "https://academyopen.ru/api-7/news/898",
    "https://academyopen.ru/api-7/news/899",
    "https://academyopen.ru/api-7/news/897",
    "https://academyopen.ru/api-7/news/896",
    "https://academyopen.ru/api-7/news/895",
    "https://academyopen.ru/api-7/news/894",
    "https://academyopen.ru/api-7/news/893",
    "https://academyopen.ru/api-7/news/892",
    "https://academyopen.ru/api-7/news/891",
    "https://academyopen.ru/api-7/news/890",
    "https://academyopen.ru/api-7/news/889",
    "https://academyopen.ru/api-7/news/888",
    "https://academyopen.ru/api-7/news/886",
    "https://academyopen.ru/api-7/news/885",
    "https://academyopen.ru/api-7/news/884",
    "https://academyopen.ru/api-7/news/883",
    "https://academyopen.ru/api-7/news/882",
    "https://academyopen.ru/api-7/news/880",
    "https://academyopen.ru/api-7/news/879",
    "https://academyopen.ru/api-7/news/878",
    "https://academyopen.ru/api-7/news/877",
    "https://academyopen.ru/api-7/news/876",
    "https://academyopen.ru/api-7/news/873",
    "https://academyopen.ru/api-7/news/872",
    "https://academyopen.ru/api-7/news/871",
    "https://academyopen.ru/api-7/news/870",
    "https://academyopen.ru/api-7/news/869",
    "https://academyopen.ru/api-7/news/865",
    "https://academyopen.ru/api-7/news/860",
    "https://academyopen.ru/api-7/news/863",
    "https://academyopen.ru/api-7/news/861",
    "https://academyopen.ru/api-7/news/859",
    "https://academyopen.ru/api-7/news/858",
    "https://academyopen.ru/api-7/news/854",
    "https://academyopen.ru/api-7/news/853",
    "https://academyopen.ru/api-7/news/852",
    "https://academyopen.ru/api-7/news/848",
    "https://academyopen.ru/api-7/news/843",
    "https://academyopen.ru/api-7/news/834",
    "https://academyopen.ru/api-7/news/841",
    "https://academyopen.ru/api-7/news/845",
    "https://academyopen.ru/api-7/news/842",
    "https://academyopen.ru/api-7/news/839",
    "https://academyopen.ru/api-7/news/837",
    "https://academyopen.ru/api-7/news/835",
    "https://academyopen.ru/api-7/news/831",
    "https://academyopen.ru/api-7/news/830",
    "https://academyopen.ru/api-7/news/829",
    "https://academyopen.ru/api-7/news/828",
    "https://academyopen.ru/api-7/news/827",
    "https://academyopen.ru/api-7/news/826",
    "https://academyopen.ru/api-7/news/824",
    "https://academyopen.ru/api-7/news/823",
    "https://academyopen.ru/api-7/news/812",
    "https://academyopen.ru/api-7/news/810",
    "https://academyopen.ru/api-7/news/802",
    "https://academyopen.ru/api-7/news/807",
    "https://academyopen.ru/api-7/news/805",
    "https://academyopen.ru/api-7/news/799",
    "https://academyopen.ru/api-7/news/804",
    "https://academyopen.ru/api-7/news/800",
    "https://academyopen.ru/api-7/news/798",
    "https://academyopen.ru/api-7/news/797",
    "https://academyopen.ru/api-7/news/795",
    "https://academyopen.ru/api-7/news/786",
    "https://academyopen.ru/api-7/news/784",
    "https://academyopen.ru/api-7/news/783",
    "https://academyopen.ru/api-7/news/782",
    "https://academyopen.ru/api-7/news/781",
    "https://academyopen.ru/api-7/news/780",
    "https://academyopen.ru/api-7/news/775",
    "https://academyopen.ru/api-7/news/773",
    "https://academyopen.ru/api-7/news/772",
    "https://academyopen.ru/api-7/news/771",
    "https://academyopen.ru/api-7/news/770",
    "https://academyopen.ru/api-7/news/763",
    "https://academyopen.ru/api-7/news/767",
    "https://academyopen.ru/api-7/news/766",
    "https://academyopen.ru/api-7/news/765",
    "https://academyopen.ru/api-7/news/764",
    "https://academyopen.ru/api-7/news/760",
    "https://academyopen.ru/api-7/news/754",
    "https://academyopen.ru/api-7/news/758",
    "https://academyopen.ru/api-7/news/756",
    "https://academyopen.ru/api-7/news/748",
    "https://academyopen.ru/api-7/news/746",
    "https://academyopen.ru/api-7/news/745",
    "https://academyopen.ru/api-7/news/739",
    "https://academyopen.ru/api-7/news/735",
    "https://academyopen.ru/api-7/news/733",
    "https://academyopen.ru/api-7/news/728",
    "https://academyopen.ru/api-7/news/726",
    "https://academyopen.ru/api-7/news/718",
    "https://academyopen.ru/api-7/news/715",
    "https://academyopen.ru/api-7/news/709",
    "https://academyopen.ru/api-7/news/703",
    "https://academyopen.ru/api-7/news/702",
    "https://academyopen.ru/api-7/news/701",
    "https://academyopen.ru/api-7/news/699",
    "https://academyopen.ru/api-7/news/687",
    "https://academyopen.ru/api-7/news/678",
    "https://academyopen.ru/api-7/news/684",
    "https://academyopen.ru/api-7/news/681",
    "https://academyopen.ru/api-7/news/679",
    "https://academyopen.ru/api-7/news/676",
    "https://academyopen.ru/api-7/news/675",
    "https://academyopen.ru/api-7/news/673",
    "https://academyopen.ru/api-7/news/671",
    "https://academyopen.ru/api-7/news/669",
    "https://academyopen.ru/api-7/news/659",
    "https://academyopen.ru/api-7/news/657",
    "https://academyopen.ru/api-7/news/642",
    "https://academyopen.ru/api-7/news/637",
    "https://academyopen.ru/api-7/news/633",
    "https://academyopen.ru/api-7/news/626",
    "https://academyopen.ru/api-7/news/627",
    "https://academyopen.ru/api-7/news/622",
    "https://academyopen.ru/api-7/news/617",
    "https://academyopen.ru/api-7/news/608",
    "https://academyopen.ru/api-7/news/601",
    "https://academyopen.ru/api-7/news/599",
    "https://academyopen.ru/api-7/news/600",
    "https://academyopen.ru/api-7/news/569",
    "https://academyopen.ru/api-7/news/567",
    "https://academyopen.ru/api-7/news/565",
    "https://academyopen.ru/api-7/news/562",
    "https://academyopen.ru/api-7/news/561",
    "https://academyopen.ru/api-7/news/535",
    "https://academyopen.ru/api-7/news/529",
    "https://academyopen.ru/api-7/news/528",
    "https://academyopen.ru/api-7/news/527",
    "https://academyopen.ru/api-7/news/523",
    "https://academyopen.ru/api-7/news/512",
    "https://academyopen.ru/api-7/news/510",
    "https://academyopen.ru/api-7/news/508",
    "https://academyopen.ru/api-7/news/502",
    "https://academyopen.ru/api-7/news/501",
    "https://academyopen.ru/api-7/news/505",
    "https://academyopen.ru/api-7/news/499",
    "https://academyopen.ru/api-7/news/498",
    "https://academyopen.ru/api-7/news/494",
    "https://academyopen.ru/api-7/news/492",
    "https://academyopen.ru/api-7/news/491",
    "https://academyopen.ru/api-7/news/488",
    "https://academyopen.ru/api-7/news/484",
    "https://academyopen.ru/api-7/news/480",
    "https://academyopen.ru/api-7/news/479",
    "https://academyopen.ru/api-7/news/478",
    "https://academyopen.ru/api-7/news/474",
    "https://academyopen.ru/api-7/news/471",
    "https://academyopen.ru/api-7/news/470",
    "https://academyopen.ru/api-7/news/469",
    "https://academyopen.ru/api-7/news/466",
    "https://academyopen.ru/api-7/news/464",
    "https://academyopen.ru/api-7/news/463",
    "https://academyopen.ru/api-7/news/458",
    "https://academyopen.ru/api-7/news/454",
    "https://academyopen.ru/api-7/news/453",
    "https://academyopen.ru/api-7/news/441",
    "https://academyopen.ru/api-7/news/438",
    "https://academyopen.ru/api-7/news/437",
    "https://academyopen.ru/api-7/news/436",
    "https://academyopen.ru/api-7/news/435",
    "https://academyopen.ru/api-7/news/431",
    "https://academyopen.ru/api-7/news/432",
    "https://academyopen.ru/api-7/news/428",
    "https://academyopen.ru/api-7/news/427",
    "https://academyopen.ru/api-7/news/423",
    "https://academyopen.ru/api-7/news/426",
    "https://academyopen.ru/api-7/news/424",
    "https://academyopen.ru/api-7/news/420",
    "https://academyopen.ru/api-7/news/418",
    "https://academyopen.ru/api-7/news/417",
    "https://academyopen.ru/api-7/news/416",
    "https://academyopen.ru/api-7/news/405",
    "https://academyopen.ru/api-7/news/402",
    "https://academyopen.ru/api-7/news/399",
    "https://academyopen.ru/api-7/news/398",
    "https://academyopen.ru/api-7/news/395",
    "https://academyopen.ru/api-7/news/394",
    "https://academyopen.ru/api-7/news/392",
    "https://academyopen.ru/api-7/news/390",
    "https://academyopen.ru/api-7/news/388",
    "https://academyopen.ru/api-7/news/387",
    "https://academyopen.ru/api-7/news/385",
    "https://academyopen.ru/api-7/news/384",
    "https://academyopen.ru/api-7/news/373",
    "https://academyopen.ru/api-7/news/367",
    "https://academyopen.ru/api-7/news/365",
    "https://academyopen.ru/api-7/news/359",
    "https://academyopen.ru/api-7/news/355",
    "https://academyopen.ru/api-7/news/349",
    "https://academyopen.ru/api-7/news/347",
    "https://academyopen.ru/api-7/news/344",
    "https://academyopen.ru/api-7/news/341",
    "https://academyopen.ru/api-7/news/340",
    "https://academyopen.ru/api-7/news/336",
    "https://academyopen.ru/api-7/news/193",
    "https://academyopen.ru/api-7/news/192"

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
                # text_bar.update(1)
                # add_empty_line(doc)  # Вставляем пустую строку

        elif block_type == 10:  # Заголовок
            text = block.get("text")
            if text:
                add_text_block(doc, text, 16, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
                # add_empty_line(doc)
        elif block_type == 11:  # Список
            elem_list = block.get("elemList")
            if elem_list and elem_list["elemType"] == 2:
                elems = elem_list["elems"]
                if elems:
                    for elem in elems:
                        add_text_block(doc, "- " + elem, 10, alignment=WD_PARAGRAPH_ALIGNMENT.LEFT)
                    # add_empty_line(doc)
        elif block_type == 2:  # Комментарий пользователя сервиса
            text = block.get("text")
            if text:
                add_text_block(doc, text, 11, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
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
                    if sign:
                        # Добавление комментария, если он есть
                        # add_text_block(doc, "Комментарий:", 12, WD_PARAGRAPH_ALIGNMENT.LEFT)
                        add_text_block(doc, sign, 10, font_style='italic', alignment=WD_PARAGRAPH_ALIGNMENT.LEFT)
                    add_empty_line(doc)
                else:
                    # Вставка изображения в docx без комментария
                    doc.add_picture(image_path, width=Inches(6.0))  # Изменение размеров картинки
                    # add_empty_line(doc)

    # Сохранение документа названием статьи в папку с названием статьи
    doc.save(docx_filename)
    print(
        f"Документ сохранен: {docx_filename}\n------------------------------------------------------------------------------")
    json_bar.close()
