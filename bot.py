import json
import os

import requests
from requests_toolbelt import MultipartEncoder

FACEBOOK_GRAPH_URL = 'https://graph.facebook.com/v2.6/me/messages'


class Bot(object):
    def __init__(self, access_token, api_url=FACEBOOK_GRAPH_URL):
        self.access_token = access_token
        self.api_url = api_url

    def send_text_message(self, psid, message, messaging_type="RESPONSE"):
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'messaging_type': messaging_type,
            'recipient': {'id': psid},
            'message': {'text': message}
        }

        params = {'access_token': self.access_token}
        response = requests.post(self.api_url,
                                 headers=headers, params=params,
                                 data=json.dumps(data))
        print (response.content)

    def send_image(self, psid, image_path, messaging_type="RESPONSE"):
        data = {
            # encode nested json to avoid errors during multipart encoding process
            'recipient': json.dumps({
                'id': psid
            }),
            # encode nested json to avoid errors during multipart encoding process
            'message': json.dumps({
                'attachment': {
                    'type': 'image',
                    'payload': {}
                }
            }),
            'filedata': (
                os.path.basename(image_path), open(image_path, 'rb'),
                'image/png')
        }
        params = {
            'access_token': self.access_token
        }
        multipart_data = MultipartEncoder(data)
        multipart_header = {
            'Content-Type': multipart_data.content_type
        }
        data = requests.post(self.api_url, headers=multipart_header,
                             params=params,
                             data=multipart_data)
        print(data.status_code, data.content)


# bot = Bot('EAAbxRlvbDcQBAA4CH0emXbk3oEHZCDW5IcZCK2JSxEILLwm9W48iSlVyMDT3C61XofnBiwAFuXqnxKmRV1um0zdbW6NUuPL3dUPnq37ETG2a6YTXfadKYfGutiogt1lhjneeZA3WAjPEAJHjyM3meISZB4FFZBk3zxbExY615x40hhFXiBtZCfd5pxAXjebkoZD')
# bot.send_text_message(1897008127048278, 'Testing..')