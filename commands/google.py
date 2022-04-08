async def google(message):
    query = message.content.lower().split(" ")
    safe_check = query[2]
    if len(query) <= 5:
        query = "+".join(query)
        if safe_check in [
            "he",
            "she",
            "that",
            "it",
            "doing",
            "saying",
            "thinking",
            "acting",
        ]:
            return
        template = f"https://www.google.com/search?q={query}"
        await message.channel.send(template)