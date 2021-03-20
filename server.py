#import vk
from random import randint
from commander import execute


def random_id():
    return randint(1, 2147483647)


#session = vk.Session()
#api = vk.API(session, v=5.95)


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


MAX_MESSAGE_LENGTH = 1999


def message_splitter(m):
    while len(m[-1]) > MAX_MESSAGE_LENGTH:
        m.append(m[-1][MAX_MESSAGE_LENGTH:])
        m[-2] = m[-2][:MAX_MESSAGE_LENGTH]
    return m


#def send_message(peer_id, message, attachment=""):
#    message = message.replace('*', '')  # quick kostyl' because vk
#    message = message.replace('~', '')
#    api.messages.send(access_token=token_vk, peer_id=str(peer_id), message=message, attachment=attachment, random_id=random_id())


def process(data):
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
