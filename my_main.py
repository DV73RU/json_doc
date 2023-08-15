import os
import hashlib
import requests
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from io import BytesIO
import html2text

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
    print(f"Subtitle: {title}")

    # Добавление остальных данных из JSON и другие операции

    # Получение значения из поля "subtitle"
    subtitle = your_json["data"]["subtitle"]
    print(f"Subtitle: {subtitle}")

    add_text_block(doc, subtitle, 12, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)  # Подзаголовок
    add_empty_line(doc)  # Вызов функции для добавления пустой строки

    # Получение значения "materials"
    materials = your_json["data"]["materials"]
    print(f"Доп материалы: {materials}")



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
        elif block_type == 11: # Список
            elem_list = block.get("elemList")
            if elem_list and elem_list["elemType"] == 2:
                elems = elem_list["elems"]
                if elems:
                    for elem in elems:
                        add_text_block(doc, "- " + elem, 10, alignment=WD_PARAGRAPH_ALIGNMENT.LEFT)
                    add_empty_line(doc)

    # Сохранение документа названием статьи в папку с названием статьи
    doc.save(docx_filename)
    print(f"Документ сохранен: {docx_filename}")
