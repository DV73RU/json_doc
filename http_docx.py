from docx import Document
from htmldocx import HtmlToDocx

# Пример HTML-кода для вставки
html_text = "<p>This is <strong>bold</strong> text.</p> <a href=\"https://news.tpprf.ru/ru/news/4082526/\">6 марта 2023 года</a>"

# Создание объекта Document
doc = Document()

# Инициализация конвертера
html_to_docx = HtmlToDocx()

# Преобразование HTML в DOCX и вставка в документ
html_to_docx.add_html_to_document(html_text, doc)

# Сохранение документа
doc.save("output.docx")