async def retrieve_n_messages_from_chat_history(n, client, channel): 
    history = []
    async for msg in channel.history(limit=n): 
        if msg.author != client.user and "!" in msg.content.strip()[0:2]:
            history.append(msg.content)

    return history

async def get_response(command, client, db_channel, ignore_last_comment=False):
    history = await retrieve_n_messages_from_chat_history(500, client, db_channel)
    if ignore_last_comment:
        history = history[1:]
    for message in history:
        if command == message.strip().split()[0]:
            return " ".join(message.split()[1:])
    return ""
    
async def validate_faq_add(message, client, db_channel):
    maybe_response = await get_response(message.content.strip().split(" ")[0], client, db_channel, ignore_last_comment=True)
    if maybe_response != "":
        await db_channel.send(
            "ERROR: id `%s` already exists in this channel; it points to table with value ```%s```" % 
            (
                message.content.strip().split(" ")[0], 
                maybe_response
            )
        )
    if len(message.content.strip().split(" ")) < 2:
        await db_channel.send("ERROR: no value provided for id `%s`" % message.content.strip().split(" ")[0])

async def reply_to_question(message, client, db_channel):
    async with message.channel.typing():
        message_stripped = message.content.strip()
        # remove mentions
        message_stripped = message_stripped.replace("<@%s>" % client.user.id, "").strip() + " " 
        if "!" in message_stripped[0:2]:  
            command = message_stripped.split(" ")[0] 
            response = await get_response(command, client,  db_channel) 
            if response.strip() != "":
                await message.channel.send(response.strip())
