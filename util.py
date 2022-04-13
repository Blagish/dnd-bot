MAX_MESSAGE_LENGTH = 1999


def message_splitter(m):
    while len(m[-1]) > MAX_MESSAGE_LENGTH:
        # try to cut by enters first
        enter = m[-1].rfind('\n')
        while enter >= MAX_MESSAGE_LENGTH:
            enter = m[-1].rfind('\n', 0, enter)
        if enter != -1:
            m.append(m[-1][enter:])
            m[-2] = m[-2][:enter]
        else:
            m.append(m[-1][MAX_MESSAGE_LENGTH:])
            m[-2] = m[-2][:MAX_MESSAGE_LENGTH]
    return m
