import requests
from time import time


def get_server_response(url):
    response = requests.get(url)
    return response


def save_image(response):
    img_name = response.url.split('/')[-1]
    img_path = f'./img/{img_name}'
    with open(img_path, 'wb') as img:
        img.write(response.content)


def main():
    img_quantity = 10
    t0 = time()
    url = 'https://loremflickr.com/320/240'
    for i in range(img_quantity):
        response = get_server_response(url)
        save_image(response)
    total_spent = round(time() - t0, 2)
    print('Synchronously:')
    print(f"To download {img_quantity} images {total_spent} seconds spent")


if __name__ == '__main__':
    main()

