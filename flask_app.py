from flask import Flask, request, json
from config import *
import server


app = Flask(__name__)


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
        output = server.process(data)

        for message in output:
            server.send_message(peer_id, message)

        return 'ok'
