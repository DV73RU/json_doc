"""
Скрипт переименовывает ссылки в текстовом файле.
Открываем текстовый файл Fool_list.txt
Заменяем часть ссылки с /journal/ на /api-7/news/
Сохраняем новый файл с имением Fool_list_json.txt
"""
input_file = "passing_list.txt"
output_file = "passing_list_json.txt"

with open(input_file, "r") as f:
    lines = f.readlines()

new_lines = [line.replace("/journal/", "/api-7/news/") for line in lines]

with open(output_file, "w") as f:
    f.writelines(new_lines)

print("Ссылки переименованы и сохранены в файл:", output_file)
