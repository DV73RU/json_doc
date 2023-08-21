
# Открываем файл list_json.txt для чтения
with open("list_json.txt", "r") as file:
    # Читаем каждую строку файла и удаляем лишние символы перевода строки
    links = [line.strip() for line in file.readlines()]
# Проверяем, не пуст ли список ссылок
if not links:
    print("Список ссылок пуст.")
else:
    print(links)
    print(f"Количество ссылок в файле: {len(links)}")
