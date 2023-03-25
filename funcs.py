import requests


def download_comic(image_url, filename):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_url_for_vk_publication(token, vk_group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {'access_token': token,
              'group_id': vk_group_id,
              'v': '5.131'
              }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def upload_comic_to_vk_server(url, filename):
    with open(filename, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
    response.raise_for_status()
    return response.json()


def save_comic_image_to_vk(token, server, photo, image_hash, vk_group_id):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {'access_token': token,
              'group_id': vk_group_id,
              'v': '5.131',
              'server': server,
              'photo': photo,
              'hash': image_hash,
              }

    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def publish_comic_on_the_vk_page(token, comments, owner_id, media_id, vk_group_id):
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': token,
        'owner_id': f'-{vk_group_id}',
        'v': '5.131',
        'from_group': '1',
        'attachments': f'photo{owner_id}_{media_id}',
        'message': comments
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
