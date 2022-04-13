MAX_MESSAGE_LENGTH = 1999


async def ctx_send(ctx, message):
    messages = [message]
    while len(messages[-1]) > MAX_MESSAGE_LENGTH:
        messages = []
        enter = message.rfind('\n')
        while enter >= MAX_MESSAGE_LENGTH:
            enter = message.rfind('\n', 0, enter)
        if enter == -1:
            enter = MAX_MESSAGE_LENGTH
        messages.append(messages[-1][enter:])
        messages[-2] = messages[-2][:enter]

    for m in messages:
        await ctx.send(m)
