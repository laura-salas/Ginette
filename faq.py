async def retrieve_n_messages_from_chat_history(n, client, channel): 
    history = []
    async for msg in channel.history(limit=n): # As an example, I've set the limit to 10000
        if msg.author != client.user and "!" in msg.content.strip()[0:2]:
            history.append(msg.content)

    return history

async def get_response(command, client, db_channel):
    history = await retrieve_n_messages_from_chat_history(500, client, db_channel)
    for message in history:
        if command == message.strip().split()[0]:
            return " ".join(message.split()[1:])
    return ""
    

async def reply_to_question(message, client, db_channel):
    async with message.channel.typing():
        message_stripped = message.content.strip()
        if "!" in message_stripped[0:2]: 
            command = message_stripped.split(" ")[0]
            response = await get_response(command, client,  db_channel)
            if response.strip() != "":
                await message.channel.send(response.strip())
