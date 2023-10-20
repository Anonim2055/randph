import requests
from flask import jsonify


def upload(file):
    with open('cid', 'r') as t_id:
        cid = str(t_id.read())
    headers = {'Authorization': f'Client-ID {cid}'}  # it has to be "cid" file with client id for imgur in it
    response = requests.post('https://api.imgur.com/3/image', headers=headers, files={'image': file})
    # print(response)
    if response.status_code == 200:
        imgur_response = response.json()
        # print(imgur_response)
        img_url = imgur_response['data']['link']
        # print(img_url, "url")
        return {
            'img_url': img_url,
            'status': "uploaded"
        }
    else:
        print("Image upload failed. Status code:", response.status_code)
        return {
            'error': 'Image upload failed'
        }, 500
