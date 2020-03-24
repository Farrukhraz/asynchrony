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
    tests = 3
    total_time = 0
    imgs_per_iteration = 10
    for k in range(tests):
        t0 = time()
        url = 'https://loremflickr.com/320/240'
        for i in range(imgs_per_iteration):
            response = get_server_response(url)
            save_image(response)
        total_time += time() - t0
    average = round(total_time / tests, 2)
    print('Synchronously')
    print(f"Average time to download {imgs_per_iteration} images {tests} times = {average} secs.")


if __name__ == '__main__':
    main()

