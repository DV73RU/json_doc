"""
Парсим блоки json

узнать в какой новости присутствуют интересующие  блоки

"""
import requests
from tqdm import tqdm  # Импорт библиотеки tqdm

# Список ссылок
links = [
    "https://academyopen.ru/api-7/news/905",
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
    "https://academyopen.ru/api-7/news/192",
    # Добавьте остальные ссылки сюда
]

# # Проход по каждой ссылке с использованием tqdm для статус-бара
# for link in tqdm(links, desc="Парсинг url: ", unit="link"):
#     # Отправка GET-запроса к ссылке и получение JSON-данных
#     response = requests.get(link)
#     if response.status_code == 200:
#         json_data = response.json()
#
#         block_type_values = []
#
#         for block in json_data["data"]["blocks"]:
#             block_type = block["blockType"]
#             if block_type is not None:  # Основной текст
#                 # text = block.get("text")
#                 block_type_values.append(block_type)
#         if block_type_values:
#             print(f"Link: {link}")
#             print(f"BlockType values: {block_type_values}")
#             print()

block_type_values = []

# Проход по каждой ссылке
for link in tqdm(links, desc="Парсинг url: ", unit="link"):
    # Отправка GET-запроса к ссылке и получение JSON-данных
    response = requests.get(link)
    if response.status_code == 200:
        json_data = response.json()

        # Получение всех значений blockType для блоков в JSON-данных
        for block in json_data["data"]["blocks"]:
            block_type = block["blockType"]
            if block_type is not None:
                block_type_values.append(block_type)

        # Удаление дублирующихся значений и преобразование в список
        unique_block_type_values = list(set(block_type_values))

        # Вывод ссылки и списка уникальных значений blockType, если он не пустой
        if unique_block_type_values:
            print(f"Link: {link}")
            print(f"Пресутсвуют блоки: {unique_block_type_values}")
            print()
