import requests

def get_info_by_ip(ip = '127.0.0.1'):
    try:
        responce = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        print(responce)
    except requests.exceptions.ConnectionError:
        print('ConnectionError => exit')

if __name__ == '__main__':
    ip = input('Enter a IP-address: ')
    get_info_by_ip(ip=ip)