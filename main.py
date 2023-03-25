import requests
import os

from dotenv import load_dotenv
from random import randint

from funcs import download_comic, get_url_for_vk_publication, publish_comic_on_the_vk_page, \
    save_comic_image_to_vk, upload_comic_to_vk_server


def main():
    load_dotenv()
    access_token = os.environ["VK_ACCESS_TOKEN"]
    vk_group_id = os.environ['VK_GROUP_ID']
    comics_in_total = 2755
    random_comic_id = randint(1, comics_in_total)
    images_path = 'images'
    comic_filename = os.path.join(images_path, str(random_comic_id))
    comic_path = f'{comic_filename}.png'
    comic_url = f'https://xkcd.com/{random_comic_id}/info.0.json'

    try:
        comic_response = requests.get(comic_url)
        comic_response.raise_for_status()
        comic_details = comic_response.json()
        comic_comments = comic_details['alt']
        comic_image_url = comic_details['img']

        download_comic(comic_image_url, comic_path)
        url_for_vk_publication = get_url_for_vk_publication(access_token, vk_group_id)
        image_details = upload_comic_to_vk_server(url_for_vk_publication, comic_path)
        photo = image_details['photo']
        server = image_details['server']
        image_hash = image_details['hash']
        comic_vk_details = save_comic_image_to_vk(access_token, server, photo, image_hash, vk_group_id)

        dissected_image_details = comic_vk_details['response'][0]
        media_id = dissected_image_details['id']
        owner_id = dissected_image_details['owner_id']
        publish_comic_on_the_vk_page(access_token, comic_comments, owner_id, media_id, vk_group_id)

    except requests.exceptions:
        raise Exception('Error occured, please try again.')
    finally:
        os.remove(comic_path)


if __name__ == '__main__':
    main()
