import os
import hashlib
import requests
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from io import BytesIO
import html2text
from docx.shared import Inches

# Список URL для JSON данных
json_urls = [
    "https://academyopen.ru/api-7/news/903",
    "https://academyopen.ru/api-7/news/904",
    # ... добавьте другие URL-ы с JSON данными
]


def add_empty_line(doc):
    doc.add_paragraph("")


def html_to_plain_text(html):
    h = html2text.HTML2Text()
    h.ignore_links = True
    return h.handle(html)


def add_text_block(doc, text, font_size, font_style=None, alignment=WD_PARAGRAPH_ALIGNMENT.LEFT,
                   spacing_after=Pt(0)):
    paragraph = doc.add_paragraph(text)
    paragraph.alignment = alignment
    paragraph.paragraph_format.space_after = spacing_after
    run = paragraph.runs[0]
    run.font.size = Pt(font_size)
    if font_style == 'bold':
        run.font.bold = True
    elif font_style == 'italic':
        run.font.italic = True
    return paragraph


# Для каждого URL получаем JSON данные и создаем документ
for json_url in json_urls:
    response = requests.get(json_url)
    your_json = response.json()

    # Создаем папку для сохранения документов, если её еще нет
    title = your_json["data"]["title"]
    title_for_folder = title.replace('/', '_').replace(':', '_')
    folder_path = os.path.join(os.getcwd(), title_for_folder)
    os.makedirs(folder_path, exist_ok=True)
    print(f"Создана директория: {folder_path}")

    # Путь к файлу .docx внутри папки
    docx_filename = os.path.join(folder_path, f"{title_for_folder}.docx")
    print(f"Создан файл: {docx_filename}")

    # Создание документа
    doc = Document()
    doc.styles['Normal'].font.name = 'Times New Roman'

    # Добавление названия статьи
    add_text_block(doc, title, 14, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
    print(f"Title: {title}")

    # Получение значения из поля "subtitle"
    subtitle = your_json["data"]["subtitle"]
    print(f"Subtitle: {subtitle}")

    add_text_block(doc, subtitle, 12, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)  # Подзаголовок
    add_empty_line(doc)  # Вызов функции для добавления пустой строки

    # Получение значения "materials"
    materials = your_json["data"]["materials"]
    print(f"Доп материалы: {materials}")

    # Создание папки для дополнительных материалов
    materials_folder = os.path.join(folder_path, "materials")
    os.makedirs(materials_folder, exist_ok=True)

    # Получение значения "materials"
    materials = your_json["data"]["materials"]

    # Скачивание дополнительных материалов (если есть)
    if materials:
        for material in materials:
            material_name = material["name"]
            material_url = material["file"]
            material_extension = material_url.split(".")[-1]
            material_filename = f"{material_name}.{material_extension}"
            material_path = os.path.join(materials_folder, material_filename)
            material_response = requests.get(material_url)
            with open(material_path, "wb") as material_file:
                material_file.write(material_response.content)
            print(f"Дополнительный материал скачан: {material_path}")
    else:
        print("Нет дополнительных материалов.")

    # Добавление текстовых блоков из "blocks"
    for block in your_json["data"]["blocks"]:
        block_type = block["blockType"]

        if block_type == 1:
            text = block.get("text")
            if text:
                add_text_block(doc, text, 10, alignment=WD_PARAGRAPH_ALIGNMENT.LEFT)
                add_empty_line(doc)
        elif block_type == 10:
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
        elif block["blockType"] == 5 and "carousel" in block:
            carousel_images = block["carousel"]
            for index, carousel_item in enumerate(carousel_images):
                image_url = carousel_item["image"]
                image_response = requests.get(image_url)
                image_extension = image_url.split(".")[-1]
                image_hash = hashlib.md5(image_response.content).hexdigest()
                image_filename = f"carousel_{image_hash}.{image_extension}"
                image_path = os.path.join(folder_path, image_filename)
                with open(image_path, "wb") as image_file:
                    image_file.write(image_response.content)
                # downloaded_images_count += 1
                print(f"Изображение из блока 'blockType:5''carousel' сохранено: {image_path}")

                # Добавление подписи к изображению
                sign = carousel_item.get("sign")
                if sign is not None:
                    add_empty_line(doc)
                    # Вставка изображения в docx
                    doc.add_picture(image_path, width=Inches(6.0))  # Изменение размеров картинки
                    if sign:
                        # Добавление комментария, если он есть
                        add_text_block(doc, "Комментарий:", 12, WD_PARAGRAPH_ALIGNMENT.LEFT)
                        add_text_block(doc, sign, 10, font_style='italic', alignment=WD_PARAGRAPH_ALIGNMENT.LEFT)
                    add_empty_line(doc)
                else:
                    # Вставка изображения в docx без комментария
                    doc.add_picture(image_path, width=Inches(6.0))  # Изменение размеров картинки
                    add_empty_line(doc)
    # Скачивание и сохранение изображений из блока "blockType": 5 "carousel"

    # for block in your_json["data"]["blocks"]:
    #     if block["blockType"] == 5 and "carousel" in block:
    #         carousel_images = block["carousel"]
    #         for index, carousel_item in enumerate(carousel_images):
    #             image_url = carousel_item["image"]
    #             image_response = requests.get(image_url)
    #             image_extension = image_url.split(".")[-1]
    #             image_hash = hashlib.md5(image_response.content).hexdigest()
    #             image_filename = f"carousel_{image_hash}.{image_extension}"
    #             image_path = os.path.join(folder_path, image_filename)
    #             with open(image_path, "wb") as image_file:
    #                 image_file.write(image_response.content)
    #             print(f"Изображение из блока 'carousel' сохранено: {image_path}")
    #
    #             # Вставка изображения в docx
    #             doc.add_picture(image_path, width=Inches(6.0))  # Изменение размеров картинки
    #
    #             # Добавление подписи к изображению
    #             # Добавление подписи к изображению, если она есть
    #             sign = carousel_item.get("sign")
    #             if sign:
    #                 add_empty_line(doc)
    #                 add_text_block(doc, "Комментарий:", 12, WD_PARAGRAPH_ALIGNMENT.LEFT)
    #                 add_text_block(doc, sign, 10, font_style='italic', alignment=WD_PARAGRAPH_ALIGNMENT.LEFT)
    #                 add_empty_line(doc)

    # Скачивание и сохранение изображений из блока "carousel"
    # for block in your_json["data"]["blocks"]:
    #     if block["blockType"] == 5 and "carousel" in block:
    #         carousel_images = block["carousel"]
    #         for index, carousel_item in enumerate(carousel_images):
    #             image_url = carousel_item["image"]
    #             image_response = requests.get(image_url)
    #             image_extension = image_url.split(".")[-1]
    #             image_hash = hashlib.md5(image_response.content).hexdigest()
    #             image_filename = f"carousel_{image_hash}.{image_extension}"
    #             image_path = os.path.join(folder_path, image_filename)
    #             with open(image_path, "wb") as image_file:
    #                 image_file.write(image_response.content)
    #             # downloaded_images_count += 1
    #             print(f"Изображение из блока 'carousel' сохранено: {image_path}")
    #
    #             # Добавление подписи к изображению
    #             sign = carousel_item.get("sign")
    #             if sign is not None:
    #                 add_empty_line(doc)
    #                 # Вставка изображения в docx
    #                 doc.add_picture(image_path, width=Inches(6.0))  # Изменение размеров картинки
    #                 add_empty_line(doc)
    #                 # Добавление комментария, если он есть
    #                 add_text_block(doc, "Комментарий:", 12, WD_PARAGRAPH_ALIGNMENT.LEFT)
    #                 add_text_block(doc, sign, 10, font_style='italic', alignment=WD_PARAGRAPH_ALIGNMENT.LEFT)
    #                 add_empty_line(doc)

    # Сохранение документа названием статьи в папку с названием статьи
    doc.save(docx_filename)
    print(f"Документ сохранен: {docx_filename}\n------------------------------------------------------------------------------")
