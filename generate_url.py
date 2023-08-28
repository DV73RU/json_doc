# generate_url.py
"""
Генерируем список url.
ID статей начинается с 415, заканчивается  696
"""

start_number = 415
end_number = 969
base_url = 'https://academyopen.ru/api-7/news/'

# Создаем список ссылок с добавленными цифрами
links_with_numbers = [f"{base_url}{number}" for number in range(start_number, end_number + 1)]

# Сохраняем результат в текстовом файле
output_file_path = 'links_with_numbers.txt'
with open(output_file_path, 'w') as f:
    for link in links_with_numbers:
        f.write(f"{link}\n")

print(f"Ссылки с цифрами были сохранены в файл: {output_file_path}")