MAX_MESSAGE_LENGTH = 1999


async def send_long_message(ctx, message, reply=False):
    messages = [message]
    while len(message := messages[-1]) > MAX_MESSAGE_LENGTH:
        enter = message.rfind("\n")
        while enter >= MAX_MESSAGE_LENGTH:
            enter = message.rfind("\n", 0, enter)
        if enter == -1:
            enter = MAX_MESSAGE_LENGTH
        messages.append(message[enter:])
        messages[-2] = message[:enter]

    for m in messages:
        if not reply:
            await ctx.send(m)
        else:
            await ctx.reply(m)
