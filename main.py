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

domen = 'http://health-diet.ru'
url = 'http://health-diet.ru/table_calorie/'

#____________________________________________________
# вытаскиваем заголовки продуктов с сайта
# response = requests.get(url)
# # print(response.status_code)
# src = response.text # html структура сайта

# with open("core/html/index.html", 'w') as file:
#     file.write(src)
#_________________________________________________________________________

#Спарсили названия заголовков и их ссылки

# with open("core/html/index.html", 'r') as file:
#     src = file.read()
    
# # find - для того чтобы вытащить тег
# #get - для того чтобы выташить параметр тега

# # a = BeautifulSoup(src, "html").find("")
# # print(a)

# soup = BeautifulSoup(src, "html.parser")
# all_products = soup.find_all(class_="mzr-tc-group-item-href")
# # вытащили названия заголовков с тегами
# # print(all_products)

# all_categories_dict = {}

# for item in all_products:
#     item_text = item.text
#     item_url = domen + item.get("href")
#     # print(f'{item_text} : {item_url}')
#     all_categories_dict[item_text] = item_url

# #dump - метод записи в json файл
# #indent - отступы в файле
# #ensure_ascii - перевод формата на английский
# with open(f"core/json/all_categories_dict.json", 'w') as file:
#     json.dump(all_categories_dict, file, ensure_ascii=False, indent=4)
#________________________________________________________________________

with open(f"core/json/all_categories_dict.json", 'r') as file:
    all_categories = json.load(file)

count = 0
iter_count = int(len(all_categories)) - 1

for categorie_name, categorie_url in all_categories.items():
    # print(f"{categorie_name}")
    # print(f"{categorie_url}")
    rep = [" ", "-", ",", "'"]
    for item in categorie_name:
        if item in rep:
            categorie_name = categorie_name.replace(item, "_")
    # print(categorie_name)
    
    response = requests.get(url=categorie_url, headers=headers)
    src = response.text
    
    with open(f"core/html/{count}_{categorie_name}.html", "w") as file:
        file.write(src)
        
    with open(f"core/html/{count}_{categorie_name}.html", "r") as file:
        src = file.read()
        
    soup = BeautifulSoup(src, "html.parser")
    
    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue
    
    # вытаскиваем заголовки таблицы 
    
    table_header = soup.find(class_="mzr-tc-group-table").find("tr").find_all('th')
    product = table_header[0].text
    calories = table_header[1].text
    proteins = table_header[2].text
    fats = table_header[3].text 
    carbons = table_header[4].text 
    
    # print(product, calories, proteins, fats, carbons)
    with open(f"core/csv/{count}_{categorie_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file) #writer - чтобы записать файл csv 
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbons,
            )
        )
    
    # собираем данные продуктов
    product_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all('tr')
    
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
            "carbons": product_carbohydrates
            }
        )
    
        with open(f"core/csv/{count}_{categorie_name}.csv", 'a', encoding="utf-8") as file:
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
    with open(f"core/json/{count}_{categorie_name}.json", 'w', encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)
    
    count += 1
    print(f"Проход по {count} и {categorie_name} записан...")
    
    iter_count = iter_count - 1
    if iter_count == 0:
        print("Работа программы завершена!")
        break
    
    print(f"осталось еще {iter_count} итераций")
    sleep(random.randrange(2, 4))