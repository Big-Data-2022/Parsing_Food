#pip install bs4 requests lxml
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
# #headers  нужен для того чтобы нас не подумали что мы боты. при парсинге

domen = "https://health-diet.ru"
url = "https://health-diet.ru/table_calorie/"

# #__________________________________________________________
# # __
# # мы тут вытащили заголовки 
# response = requests.get(url)
# # print(response.text)
# src = response.text
# #____________________________________________________________

# #вытащили(спарсили ) заголовку и ссылки


# with open ("core/html/index.html", "w")as file:
#     file.write(src)

# with open ("core/html/index.html", "r")as file:
#     src = file.read()

# soup = BeautifulSoup(src, 'lxml')
# all_products = soup.find_all(class_="mzr-tc-group-item-href")
# #мы тут вытащили все заголовки сайта с тегами
# print(all_products)

# all_categories_dict = {}

# for item in all_products:

#     item_text = item.text
#     item_url = domen + item.get("href")
#     print(f'{item_text}:{item_url}')
#     all_categories_dict[item_text] = item_url

# with open (f"core/json/all_categories_dict.json", "w") as file:
#     json.dump(all_categories_dict, file,indent=4, ensure_ascii=False)

# #lxml будет быстро орабатывать информацию (может парсить приложения ,сайты )
# all_product = soup.title
# print(src)

# a = BeautifulSoup(src,"lxml").find("link").get("href")
# # find для того чтобы вытащить тег
# # get  для того чтобы вытащить параметр тега 
# print(a)

# a = BeautifulSoup(src,"lxml").find("div").find_all("")
# #______________________________________________________________________________________

with open (f"core/json/all_categories_dict.json", "r") as file:
    all_categories = json.load(file)
    #load метод который вытаскивает
    #dump записивыет

iter_count = int(len(all_categories)) - 1
count = 0

for category_name, category_url in all_categories.items():
    # print(f"{category_name}")
    # print(f"{category_url}")

    rep = [",", " ", "-", "'"]
    for item in category_name:
        if item in rep:
            category_name = category_name.replace(item, "_")
    # print(category_name)

    response = requests.get(url=category_url, headers=headers)
    src = response.text
    with open (f"core/html/{count}_{category_name}.html", "w") as file:
        file.write(src)

    with open (f"core/html/{count}_{category_name}.html", "r") as file:
        src = file.read()
    
    soup = BeautifulSoup(src, 'lxml')

    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue
        # собираем заголовки таблицы
    table_header = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
#find_all  все засунет в лист 
    product = table_header[0].text
    calories = table_header[1].text
    proteins = table_header[2].text
    fats = table_header[3].text
    carbohydrates = table_header[4].text
    # print(product, calories,proteins,fats)

#чтобы записать в эксель файл ссв
    with open (f"core/csv/{count}_{category_name}.csv", "w",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
            product,
            calories,
            proteins,
            fats,
            carbohydrates,
            )
        )
    #writerow 
# собираем  данные продуктов
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
                "calories": product_calories,
                "proteins": product_proteins,
                "fats": product_fats,
                "carbohydrates": product_carbohydrates
            }
        )
    
        with open(f"core/csv/{count}_{category_name}.csv","a",encoding="utf-8") as file :
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
    with open (f"core/json/{count}_{category_name}.json", "w", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)
    count+=1

    print(f"проход по {count}. и {category_name} записан ... ")

    iter_count = iter_count - 1
    if iter_count == 0:
        print ("РАБОТА ВЫПОЛНЕНА")
        break

    print(f"осталось итерации : {iter_count} ")
    sleep(random.randrange(2, 4))