import vk
from config import *
from random import randint
from commander import execute


def random_id():
    return randint(1, 2147483647)


session = vk.Session()
api = vk.API(session, v=5.95)


def cut_appeal(command):
    if command == '' or command == '/':
        return None
    if command[0] == '/':
        command = command[1:]
    if command[0] == '[':
        command = command[command.index(']') + 1:]
    while command[0] == ' ':
        command = command[1:]
    return command.lower()


def message_splitter(m):
    while len(m[-1]) > 4095:
        m.append(m[-1][4095:])
        m[-2] = m[-2][:4095]
    return m


def send_message(peer_id, message, attachment=""):
    message = message.replace('*', '')  # quick kostyl' because vk
    message = message.replace('~', '')
    api.messages.send(access_token=token_vk, peer_id=str(peer_id), message=message, attachment=attachment, random_id=random_id())


def process(data):
    #fwd_msg = list(map(lambda x: x['text'], data['object']['fwd_messages']))
    #        if event.object.reply_message:
    #            fwd_msg = [event.object.reply_message['text']]
    output = []
    output_m = []
    for command in data.split(';'):
        print("received command", command)
        try:
            command = cut_appeal(command)
            print("cutted command", command)
            if command:
                output += execute(command)
        except Exception as e:
            output += [["uwu"]]
            args = list(map(str, e.args))
            print("Exception {0}: {1}".format(str(type(e)), " ".join(args)))
            #
            # output += ["Exception {0}: {1}".format(str(type(e)), " ".join(args))]
    for message in output:
        if message:
            output_m += message_splitter(message)

    return output_m
