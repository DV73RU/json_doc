def read_links_from_file(file_path):
    links = []
    with open(file_path, "r") as file:
        links = [line.strip() for line in file.readlines()]

    if not links:
        print("Список ссылок пуст.")

    return links
