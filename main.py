import requests
import os

from contextlib import suppress
from dotenv import load_dotenv
from random import choice

from funcs import download_comics, get_url_for_vk_publication, publish_comics_on_the_vk_page, \
    upload_comics_to_vk_page, upload_comics_to_vk_server


def main():
    load_dotenv()
    access_token = os.environ["VK_ACCESS_TOKEN"]
    comics_ids = [comics_id for comics_id in range(2754)]
    random_comics_id = choice(comics_ids)
    images_path = 'images'
    comics_filename = f'{images_path}/{random_comics_id}.png'
    comics_url = f'https://xkcd.com/{random_comics_id}/info.0.json'

    with suppress(requests.exceptions):
        comics_response = requests.get(comics_url)
        comics_response.raise_for_status()
        comics_details = comics_response.json()
        comics_comments = comics_details['alt']
        comics_image_url = comics_details['img']

        download_comics(comics_image_url, comics_filename)
        url_for_vk_publication = get_url_for_vk_publication(access_token)
        image_details = upload_comics_to_vk_server(url_for_vk_publication, comics_filename)
        comics_vk_details = upload_comics_to_vk_page(image_details, access_token)

        publish_comics_on_the_vk_page(comics_vk_details, access_token, comics_comments)
        os.remove(comics_filename)


if __name__ == '__main__':
    main()
