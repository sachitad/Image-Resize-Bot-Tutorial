import json

from flask import Flask, request

from bot import Bot
from db import create_entry, get_entry, delete_entry
from utils import check_width_height_syntax, resize_image

PAGE_ACCESS_TOKEN = 'EAAbxRlvbDcQBAA4CH0emXbk3oEHZCDW5IcZCK2JSxEILLwm9W48iSlVyMDT3C61XofnBiwAFuXqnxKmRV1um0zdbW6NUuPL3dUPnq37ETG2a6YTXfadKYfGutiogt1lhjneeZA3WAjPEAJHjyM3meISZB4FFZBk3zxbExY615x40hhFXiBtZCfd5pxAXjebkoZD'
GREETINGS = ['hi', 'hello', 'howdy', 'how are you']


app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == 'secret':
            return str(challenge)
        return '400'

    else:
        data = json.loads(request.data)
        print (data)
        messaging_events = data['entry'][0]['messaging']
        bot = Bot(PAGE_ACCESS_TOKEN)
        for message in messaging_events:
            user_id = message['sender']['id']
            text_input = message['message'].get('text')
            response_text = 'I am still learning'
            if text_input in GREETINGS:
                response_text = 'Hello. Welcome to my first bot!'

            elif check_width_height_syntax(text_input) is True:
                image_url = get_entry(user_id)
                if image_url is None:
                    response_text = 'Please upload image first'
                else:
                    bot.send_text_message(user_id, '..Processing your image..')
                    resize_image(image_url, text_input)
                    bot.send_image(user_id, 'output.png')
                    bot.send_text_message(user_id, 'You are all set')
                    delete_entry(user_id)
                    return '200'
            else:
                attachments = message['message'].get('attachments')
                if attachments:
                    attachment = attachments[0]
                    attachment_type = attachment.get('type')
                    if attachment_type == 'image':
                        create_entry(user_id, (attachment.get('payload', {}).get('url')))
                        response_text = 'Thanks. I will help you resize. Tell me the size in width x height(200x100)'

            print ('Message from user ID {} - {}'.format(user_id, text_input))
            bot.send_text_message(user_id, response_text)

        return '200'



if __name__ == '__main__':
    app.run(debug=True)
