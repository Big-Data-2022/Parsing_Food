import requests
from bs4 import BeautifulSoup

import json
import csv

import random
from time import sleep

#headers - ltkfc
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
}

domen = "http://health-diet.ru"
url = "http://health-diet.ru/table_calorie/"


# Вытаскиваем заголовки продуктов 
# response = requests.get(url, headers=headers)
# # print(response.text)

# src = response.text

# with open ("core/html/index.html", "w") as file:
#     file.write(src)
#_______________________________________________________________________________

# # Спарсили название заголовков и их ссылки 

# with open ("core/html/index.html", "r") as file:
#     src = file.read()

# soup = BeautifulSoup(src, "lxml")# lxml обрабатывается быстро, используется для парсинга 
# all_product = soup.title

# # a = BeautifulSoup(src, "lxml").find("link").get("href")#обращаемя к пораметру с помощью get,
# # #чтобы вытащить теги используем find 
# # print(a)

# soup = BeautifulSoup(src, "lxml")
# all_products = soup.find_all(class_ ="mzr-tc-group-item-href")#  вытащили заголовкиБ не обработанные 

# all_cotigories_dist = {}

# for item in all_products:
#     item_text = item.text
#     item_url = domen + item.get("href")
#     # print(f"{item_text} : {item_url}")
#     all_cotigories_dist[item_text] = item_url


# with open(f"core/json/all_cotigories_dict.json", "w") as file:
#     json.dump(all_cotigories_dist, file, indent=4,  ensure_ascii=False)
# # indent - отступы 
# # ensure_ascii - если не отключить то будут проблемы с кодировкой 
# # dump - записать 

#_____________________________________________________________________________________

with open(f"core/json/all_cotigories_dict.json", "r") as file:
    all_cotigories = json.load(file)

iter_count = int(len(all_cotigories)) - 1
count = 0

for cotigories_name, cotigories_url in all_cotigories.items():
    # print(f"{cotigories_name}")
    # print(f"{cotigories_url}")

    rep = [",", " ", "-", "'"]
    for item in cotigories_name:
        if item in rep:
            cotigories_name = cotigories_name.replace(item, "_")
    # print(cotigories_name)
    response = requests.get(url=cotigories_url, headers=headers)
    src = response.text

    with open (f"core/html/{count}_{cotigories_name}.html", "w") as file:
        file.write(src)
    
    with open (f"core/html/{count}_{cotigories_name}.html", "r") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    alert_block = soup.find(class_ = "uk-alert-danger")
    if alert_block is not None:
        continue

#Собираем заголовки таблицы 
    table_header = soup.find(class_ = "mzr-tc-group-table").find("tr").find_all("th")

    product = table_header[0].text
    colories = table_header[1].text
    protiens = table_header[2].text
    fats = table_header[3].text
    carbohydrates = table_header[4].text

# writer -  чтобы записать в csv 
    with open(f"core/csv/{count}_{cotigories_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                product,
                colories,
                protiens,
                fats,
                carbohydrates
            )
        )

    # Собираем данные продуктов 

    product_data = soup.find(class_ = "mzr-tc-group-table").find("tbody").find_all("tr")
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
                "calories": product_calories,
                "proteins": product_proteins,
                "fats": product_fats,
                "carbohydrates": product_carbohydrates
            }
        )

        with open(f"core/csv/{count}_{cotigories_name}.csv", "a", encoding="utf-8") as file:
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
        
    with open(f"core/json/{count}_{cotigories_name}.json", "w", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count +=1
    print(f"Проход по {count}, и {cotigories_name} записан")


    iter_count = iter_count - 1
    if iter_count == 0:
        print("Работа выполнина ")
        break

    print(f"Осталось итерации:{iter_count}")
    sleep(random.randrange(2, 4))