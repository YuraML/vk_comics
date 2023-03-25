import requests
import os

from dotenv import load_dotenv
from random import randint

from funcs import download_comic, get_url_for_vk_publication, publish_comic_on_the_vk_page, \
    upload_comic_to_vk_page, upload_comic_to_vk_server


def main():
    load_dotenv()
    access_token = os.environ["VK_ACCESS_TOKEN"]
    comics_in_total = 2755
    random_comics_id = randint(1, comics_in_total)
    images_path = 'images'
    comics_filename = os.path.join(images_path, str(random_comics_id))
    comics_path = f'{comics_filename}.png'
    comics_url = f'https://xkcd.com/{random_comics_id}/info.0.json'

    try:
        comics_response = requests.get(comics_url)
        comics_response.raise_for_status()
        comics_details = comics_response.json()
        comics_comments = comics_details['alt']
        comics_image_url = comics_details['img']

        download_comic(comics_image_url, comics_path)
        url_for_vk_publication = get_url_for_vk_publication(access_token)
        image_details = upload_comic_to_vk_server(url_for_vk_publication, comics_path)
        comics_vk_details = upload_comic_to_vk_page(image_details, access_token)
        publish_comic_on_the_vk_page(comics_vk_details, access_token, comics_comments)
    except requests.exceptions:
        raise Exception('Error occured, please try again.')
    finally:
        os.remove(comics_path)


if __name__ == '__main__':
    main()
