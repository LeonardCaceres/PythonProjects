import requests
from bs4 import BeautifulSoup
import random
import os
from urllib.parse import urljoin
import time 

def check_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if "Страница не найдена :-(" in soup.get_text():
        return False, None
    else:
        img_tag = soup.find('img', {'id': 'image'})
        if img_tag:
            img_url = urljoin(url, img_tag['src'])
            return True, img_url
        else:
            return False, None

def download_image(img_url, folder_path, counter):
    response = requests.get(img_url)
    img_name = f"{counter}.jpg"
    img_path = os.path.join(folder_path, img_name)
    with open(img_path, 'wb') as f:
        f.write(response.content)
    print(f"Изображение {counter} успешно скачано и сохранено в", img_path)

def generate_url():
    return "https://imageup.ru/" + str(random.randint(4100000, 4638514))

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def main():
    folder_name = "downloaded_images"
    create_folder(folder_name)
    counter = 1

    while True:
        url = generate_url()
        found, img_url = check_page(url)
        if found:
            print("Найдена страница:", url)
            download_image(img_url, folder_name, counter)
            counter += 1
            time.sleep(1)
        else:
            print("Страница не найдена, пробуем следующую.")

if __name__ == "__main__":
    main()
