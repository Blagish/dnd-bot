import vk_api.vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from random import randint
from commander import execute


def random_id():
    return randint(1, 2147483647)


def message_splitter(s):
    m = [s]
    while len(m[-1]) > 4095:
        m.append(m[-1][4095:])
        m[-2] = m[-2][:4095]
    return m


class Server:

    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=api_token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()

    def send_msg(self, send_id, message):
        self.vk_api.messages.send(peer_id=send_id,
                                  message=message,
                                  random_id=random_id())

    def start(self):
        for event in self.long_poll.listen():  # Слушаем сервер
            if event.type == VkBotEventType.MESSAGE_NEW:
                fwd_msg = list(map(lambda x: x['text'], event.object.fwd_messages))
                if event.object.reply_message:
                    fwd_msg = [event.object.reply_message['text']]
                print(fwd_msg)
                output = []
                for command in event.object.text.split(';'):
                    print("received command", command);
                    try:
                        output += execute(command, fwd_msg)
                    except Exception as e:
                        args = list(map(str, e.args))
                        output += ["Exception {0}: {1}".format(str(type(e)), " ".join(args))]
                if output:
                    for message in output:
                        if message:
                            output_m = message_splitter(message)
                            for m in output_m:
                                self.send_msg(event.object.peer_id, m)

    def test(self):
        self.send_msg(121469320, "test test test")
