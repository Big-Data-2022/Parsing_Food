# pip install bs4 requests lxml

import requests
from bs4 import BeautifulSoup

import json
import csv


import random
from time import sleep

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
}

domen = "http://health-diet.ru"
url ="http://health-diet.ru/table_calorie/"


# Мы тут вытащили заголовки 
# response = requests.get(url, headers=headers)

# print(response.text)

# src = response.text

# with open("core/html/index.html","w") as file:
#     file.write(src)

# with open("core/html/index.html","r") as file:
#     src = file.read()
# print(src)
# soup = BeautifulSoup(src, "lxml")
# all_products = soup.find_all(class_ = "mzr-tc-group-item-href")
# Вытащили заголовки с тегами!
# print(all_products)

# all_categories_dict = {

# }

# for item in all_products:
#     item_text = item.text
#     item_url = domen + item.get("href")
#     # print(f"{item_url} : {item_text}")

#     all_categories_dict [item_text] = item_url

# with open (f"core/json/all_categories_dict.json", "w") as file:
#     json.dump(all_categories_dict, file,indent=4, ensure_ascii=False)


# a = BeautifulSoup(src, "lxml").find("div")
# print(a)


with open (f"core/json/all_categories_dict.json", "r") as file:
    all_categories = json.load(file)

iter_count = int(len(all_categories)) - 1
count = 0
for categories_name, categories_url in all_categories.items():
    # print(f"{categories_name}")
    # print(f"{categories_url}")

    rep = [",",".","-","'"," "]
    for item in categories_name:
        if item in rep:
            categories_name = categories_name.replace(item, "_")
    # print(categories_name)

    response = requests.get(url=categories_url, headers=headers)
    src = response.text
    
    with open(f"core/html/{count}_{categories_name}.html", "w") as file:
        file.write(src)

    with open(f"core/html/{count}_{categories_name}.html", "r") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue

    # Sobyraem zagolovki
    table_header = soup.find(class_ = "mzr-tc-group-table").find("tr").find_all("th")

    products = table_header[0].text
    calories =table_header[1].text
    proteins = table_header[2].text
    fats = table_header[3].text
    carbohydrates = table_header[4].text
    # print(products, calories, proteins, fats, carbohydrates) 

    with open(f"core/csv/{count}_{categories_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow((
            products,
            calories,
            proteins,
            fats,
            carbohydrates))

    product_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

    product_info = []

    for item in product_data:
        product_info_item = item.find_all("td")

        product_name = product_info_item[0].text
        product_calories = product_info_item[1].text
        product_proteins = product_info_item[2].text
        product_fats = product_info_item[3].text
        product_carbohydrates = product_info_item[4].text

        product_info.append(
        {
            "name": product_name,
            "calories":product_calories,
            "proteins": product_proteins,
            "fats": product_fats,
            "carbohydrates": product_carbohydrates
        }
    )

    with open(f"core/csv/{count}_{categories_name}.csv", "a", encoding="utf-8",) as file:
        writer = csv.writer(file)
            
        writer.writerow(
                (
                    product_name,
                    product_calories,
                    product_proteins,
                    product_fats,
                    product_carbohydrates,
                )
            )
    with open(f"core/json/{count}_{categories_name}.json", "w",encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f"Проход по {count}. и {categories_name} записан...")

    iter_count = iter_count - 1
    if iter_count == 0:
        print(f"Работа выполнена")
        break
        
    print(f"Осталось итерации:{iter_count}")
    sleep(random.randrange(2,4))