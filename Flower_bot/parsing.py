import requests
from bs4 import BeautifulSoup
import time
import json

PRODUCTS = {}

def get_info(url,i):
    global PRODUCTS
    req = requests.get(url=url)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    name = soup.find('h4').text.replace(' ','_').replace('/','')
    with open(f'data\{i}_{name}.html', 'w', encoding="utf-8") as file:
        file.write(src)
    with open(f'data\{i}_{name}.html',encoding="utf-8") as file:
        src = file.read()
    with open('data/names.txt', 'a', encoding="utf-8") as file:
        file.write(name + '\n')
    try:
        products = soup.find('ul', class_="grid", id="product_list").find_all('h3')
        list_to_append = []
        for product in products:
            list_to_append.append(product.text)
        list_to_append.sort()
        PRODUCTS[name] = list_to_append
    except:
        PRODUCTS[name] = 'Страница пуста'

def information():
    for i in range(4, 43):
        print(f'Accepted {i - 3}/{39}')
        if i == 13 or i == 9 or i == 27 or i == 22:     ### "duplicate pages"
            continue
        url = f'http://gfcc.ru/catalog/?search=&category_id={i}&product_from=&product_color=&product_spec=&cat_perpage=1000000&prod_sort='
        get_info(url, i)
        time.sleep(0.6)
    print(PRODUCTS)
    with open("info_dict.json", "w", encoding="utf-8") as file:
        json.dump(PRODUCTS, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    information()