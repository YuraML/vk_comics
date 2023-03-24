import requests


def download_comics(image_url, filename):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_url_for_vk_publication(token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {'access_token': token,
              'group_id': '219570094',
              'v': '5.131'
              }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def upload_comics_to_vk_server(url, filename):
    with open(filename, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()


def upload_comics_to_vk_page(image_details, token):
    photo = image_details['photo']
    server = image_details['server']
    hash = image_details['hash']

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {'access_token': token,
              'group_id': '219570094',
              'v': '5.131',
              'server': server,
              'photo': photo,
              'hash': hash,
              }

    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def publish_comics_on_the_vk_page(image_details, token, comments):
    dissected_image_details = image_details['response'][0]
    media_id = dissected_image_details['id']
    owner_id = dissected_image_details['owner_id']
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': token,
        'owner_id': '-219570094',
        'v': '5.131',
        'from_group': '1',
        'attachments': f'photo{owner_id}_{media_id}',
        'message': comments
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
