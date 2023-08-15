import os
import requests
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from io import BytesIO

# URL, где хранится JSON данные
json_url = "https://academyopen.ru/api-7/news/903"

# Список URL для JSON данных
json_urls = [
    "https://academyopen.ru/api-7/news/903",
    "https://academyopen.ru/api-7/news/904",
    "https://academyopen.ru/api-7/news/905"


]

# Создаем папку для сохранения документов, если её еще нет
if not os.path.exists("docx_files"):
    os.makedirs("docx_files")

# Для каждого URL получаем JSON данные и создаем документ
for json_url in json_urls:
    response = requests.get(json_url)
    your_json = response.json()

    # Получение значения из поля "title" для названия файла
    title = your_json["data"]["title"]
    docx_filename = f"docx_files/{title}.docx"

    # Создание документа
    doc = Document()
    doc.styles['Normal'].font.name = 'Times New Roman'


    # Функция для добавления текстового блока с заданными параметрами
    def add_text_block(text, font_size, alignment=WD_PARAGRAPH_ALIGNMENT.LEFT, spacing_after=Pt(0)):
        paragraph = doc.add_paragraph(text)
        paragraph.runs[0].font.size = Pt(font_size)
        paragraph.alignment = alignment
        paragraph.paragraph_format.space_after = spacing_after
        return paragraph


    # Функция для добавления пустой строки
    def add_empty_line():
        doc.add_paragraph("")


    # # Добавление названия рубрики
    # rubric_name = your_json["data"]["rubric"]["name"]
    # add_text_block(rubric_name, 10, WD_PARAGRAPH_ALIGNMENT.CENTER)

    # Добавление названия статьи
    title = your_json["data"]["title"]
    add_text_block(title, 14, WD_PARAGRAPH_ALIGNMENT.CENTER)
    add_empty_line()

    # Добавление СЕО описания
    # seo_title = your_json["data"]["rubric"]["seoTitle"]
    # add_text_block(seo_title, 10, WD_PARAGRAPH_ALIGNMENT.CENTER)
    # add_empty_line()
    # seo_description = your_json["data"]["rubric"]["seoDescription"]
    # add_text_block(seo_description, 10, WD_PARAGRAPH_ALIGNMENT.LEFT)
    # add_empty_line()

    # Добавление описания SEO
    seo_description = your_json["data"]["rubric"]["seoDescription"]

    # Добавляем пометку перед следующей строкой
    doc.add_paragraph("seoDescription", style='Normal')
    doc.add_paragraph(seo_description, style='Normal')  # Добавляем описание SEO

    # Добавление заголовка
    subtitle = your_json["data"]["subtitle"]
    add_text_block(subtitle, 16, WD_PARAGRAPH_ALIGNMENT.CENTER)
    add_empty_line()

    # Добавление подзаголовка
    date = your_json["data"]["date"]
    add_text_block(date, 12, WD_PARAGRAPH_ALIGNMENT.CENTER)
    add_empty_line()

    # Добавление ссылки на фото

    social_photo_url = your_json["data"]["socialPhoto"]
    response = requests.get(social_photo_url)
    image_stream = BytesIO(response.content)
    doc.add_picture(image_stream)

    # Добавление текстовых блоков из "blocks"
    for block in your_json["data"]["blocks"]:
        if block["blockType"] == 1:
            text = block["text"]
            add_text_block(text, 10)
            add_empty_line()

    # Сохранение документа в папку с названием статьи
    if not os.path.exists(title):
        os.makedirs(title)
    doc.save(os.path.join(title, docx_filename))

