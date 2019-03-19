import os
import requests

SPACE_X_API = 'https://api.spacexdata.com/v3/launches'
HUBBLE_API = 'http://hubblesite.org/api/v3/images/all'


def check_or_create_dir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)


def get_space_x_image_urls(url):
    space_resp = requests.get(SPACE_X_API).json()
    # take last succeed launch
    last_flight = (
        sorted((x for x in space_resp if x['launch_success'] == True),
               key=lambda c: c['launch_date_unix'], reverse=True)[
            0])
    return last_flight['links']['flickr_images']


def save_images_to_local_directory(dirname, image_url, name_pattern):
    for url in enumerate(image_url):
        with open((''.join([os.path.join(dirname, ''.join(
                [name_pattern, str(url[0]), '.jpg']))])), 'wb') as file:
            file.write(requests.get(url[1]).content)


def get_hubble_image_urls(url):
    hubble_resp = requests.get(HUBBLE_API).json()
    url_list = []
    image_params = []

    for image in hubble_resp:
        image_params.append(
            requests.get(
                'http://hubblesite.org/api/v3/image/' + str(
                    image['id'])).json()['image_files'])
    for param in image_params:
        url_list.append(param[0]['file_url'])
    return url_list


if __name__ == "__main__":
    check_or_create_dir('./images')
    spacex_image_url = get_space_x_image_urls(SPACE_X_API)
    save_images_to_local_directory('./images', spacex_image_url, 'spacex')
    hubble_url_list = get_hubble_image_urls(HUBBLE_API)
    save_images_to_local_directory('./images', hubble_url_list, 'hubble')
