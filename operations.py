import utils
import time
import random
from datetime import timedelta

import discord

cache = utils.loadCache()


def cache_user(author):
    global cache
    if str(author.id) not in cache.keys():
        cache[str(author.id)] = {
            "name": author.name,
            "last_command_timestamp": 0,
            "medals": 0,
            "poop": 0,
        }
    if "poop" not in cache[str(author.id)]:
        cache[str(author.id)]["poop"] = 0


def get_current_cooldown(author):
    prev_time = cache[str(author.id)]["last_command_timestamp"]
    return 15 - (int(time.time()) - prev_time)


def user_has_cooldown(author):
    time_left = get_current_cooldown(author)
    if time_left >= 0:
        return time_left


def set_cooldown(author):
    cache[str(author.id)]["last_command_timestamp"] = int(time.time())


async def lootbox(message, client, guild):
    author = message.author
    cache_user(author)
    cooldown = user_has_cooldown(author)
    if not cooldown:
        set_cooldown(author)
        res = random.choices(
            population=["slowmodeon", "slowmodeoff", "timeout", "nothing", "black"],
            weights=[0.04, 0.04, 0.20, 0.70, 0.02],
            k=1,
        )[0]
        if res == "slowmodeon":
            await handle_slowmode_more(client, message)
        if res == "slowmodeoff":
            await handle_slowmode_less(client, message)
        if res == "timeout":
            await handle_timeout(message)
        if res == "nothing":
            await handle_nothing(message)
        if res == "black":
            role = guild.get_role(944121534547640330)
            await handle_black_role(message, role)
        return
    await message.channel.send(
        f"You loser, you're on cooldown for {cooldown} more seconds."
    )


async def handle_slowmode_more(client, message):
    chet_channel = client.get_channel(336997071544385536)
    channel = message.channel
    author = message.author
    delay = chet_channel.slowmode_delay + 15
    await chet_channel.edit(slowmode_delay=delay)
    await chet_channel.send(
        f"Oh frick, {author.display_name} increased the delay on slowmode."
    )
    await channel.send(
        f"Oh boy, {author.display_name} updated slowmode in chet to {delay} seconds, thank you!"
    )


async def handle_slowmode_less(client, message):
    chet_channel = client.get_channel(336997071544385536)
    channel = message.channel
    author = message.author
    if chet_channel.slowmode_delay > 0:
        delay = chet_channel.slowmode_delay - 15
        if delay < 0:
            delay = 0
        await chet_channel.edit(slowmode_delay=delay)
        await channel.send(
            f"{author.display_name}, you have updated the slowmode in chet to {delay} seconds, guess we aren't having fun then."
        )
    else:
        await channel.send(
            f"{author.display_name}, you rolled for a slowmode decrease but its already dead! Try again."
        )


async def handle_timeout(message):
    author = message.author
    channel = message.channel
    timeout = timedelta(seconds=60)
    try:
        await author.timeout_for(timeout)
        await channel.send(
            f"Oopsie whoopsie {author.display_name} has been put in timeout!! Thats the cost of gambling."
        )
    except:
        cache[str(author.id)]["poop"] += 1
        poops = cache[str(author.id)]["poop"]
        await channel.send(
            f"{author.display_name} has won a timeout! But I wasn't able to put them in one. Instead they earned a :poop:\nLook at their nasty collection: {poops*':poop:'}"
        )
        utils.saveCache(cache)


async def handle_nothing(message):
    author = message.author
    cache[str(author.id)]["medals"] += 1
    num = cache[str(author.id)]["medals"]
    gold, rem = divmod(num, 100)
    silver, bronze = divmod(rem, 10)
    medals = (
        gold * ":first_place:" + silver * ":second_place:" + bronze * ":third_place:"
    )
    await message.channel.send(
        f"{author.display_name}, you didn't win anything, but here is a nice medal for trying: :third_place:\nHere is your collection: {medals}"
    )
    utils.saveCache(cache)


async def handle_black_role(message, role):
    author = message.author
    channel = message.channel
    if author not in role.members:
        for member in role.members:
            await member.remove_roles(role)
            await channel.send(
                f"{author.display_name} has stolen the highly cherished black role from {member.display_name}!"
            )
        await author.add_roles(role)
    else:
        await channel.send(
            f"{author.display_name}, you have been stripped of the black role. Better get rollin."
        )
        await author.remove_role(role)


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
