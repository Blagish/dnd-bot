from random import randint
from flask import Flask, request, json
from config import *
import server
import vk


app = Flask(__name__)

session = vk.Session()
api = vk.API(session, v=5.95)


def random_id():
    return randint(1, 2147483647)


def send_message(peer_id, message, attachment=""):
    message = message.replace('**', '')  # quick kostyl' because vk
    message = message.replace('~', '')
    api.messages.send(access_token=token_vk, peer_id=str(peer_id), message=message, attachment=attachment, random_id=random_id())



@app.route('/')
def main_page():
    return 'Сервер бота ВКонтакте <a href="https:/www.vk.com/dnd_bot">vk.com/dnd_bot</a>'


@app.route('/dndbot', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['secret'] != secret_token:
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        peer_id = data['object']['peer_id']
        output = server.process(data['object']['text'])

        for message in output:
            send_message(peer_id, message)

        return 'ok'
