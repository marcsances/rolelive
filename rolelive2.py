import asyncio
import json
import math
import time
import uuid
from typing import Optional, Generator
import logging


logging.basicConfig(level=logging.DEBUG)
import discord
import sys
import requests
import re
from requests.utils import quote

print("Please replace all client IDs, role IDs and tokens with the configuration you want for your server before "
      "using Rolelive for the first time, then remove this print and the inmediately following line.")
sys.exit(1)

# Polling interval
INTERVAL = 10
# Names of the roles
ROLE_NAMES = ["Test User", "Test Admin"]
# Message to show when somebody is live
MESSAGE = "%s is now live: **%s** - _%s_ - %s"
# RoleLive version
VERSION = "2.0.0"
# Discord Server ID that RoleLive will join
GUILD_ID = REPLACE_ME
# Discord valid role IDs
ROLE_IDS = [REPLACE_ME, REPLACE_ME]
# Discord admin role IDs
ADMIN_IDS = [REPLACE_ME]
# Discord admin user IDs
ADMIN_USERS = [REPLACE_ME]
# Discord bot token
DISCORD_TOKEN = 'REPLACE_ME'
# Discord notification channel ID
CHANNEL_ID = REPLACE_ME
# Time that must pass since a channel goes offline to be considered elligible for notifications again
# This prevents duplicate notifications for when a channel has technical issues
STREAM_EXPIRY = 3600
# Ignore role IDs and let anyone add their streams with no restrictions
IGNORE_ROLES = False
# Client ID for Twitch Helix API https://dev.twitch.tv/console/app
HELIX_CLIENT_ID = "CHANGE ME"
# Access token for Twitch Helix API https://dev.twitch.tv/console/app
HELIX_SECRET = "CHANGE ME"
# Items per page to ask the Helix API. Maximum according to documentations is 100 (19/02/22)
ITEMS_PER_PAGE = 99

client = discord.Client()

all_members = dict()
members_online = []
expiring = dict()


def login() -> Optional[str]:
    response = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={HELIX_CLIENT_ID}&client_secret={HELIX_SECRET}&grant_type=client_credentials")
    if response.status_code == 200:
        return response.json()["access_token"]


def generate_splits(members: Set[str]) -> List[str]:
    formatted_members = list(map(lambda m: "user_login=" + quote(m), members))
    pages = list(range(math.ceil(len(members) / ITEMS_PER_PAGE)))
    paged_members_raw = list(map(lambda page: formatted_members[ITEMS_PER_PAGE * page:ITEMS_PER_PAGE * page + ITEMS_PER_PAGE], pages))
    paged_members_filtered = filter(lambda page: len(list(page)) > 0, paged_members_raw)
    urls = list(map(lambda members_of_page: "https://api.twitch.tv/helix/streams?first=" + str(ITEMS_PER_PAGE) + "&" + "&".join(members_of_page), paged_members_filtered))
    return urls


def check_on_twitch(members: Set[str], helix_token, to_notify: List[List[str]]) -> Generator[Optional[str], None, None]:
    global members_online
    for url in generate_splits(members):
        response = requests.get(url, headers={"Client-ID": HELIX_CLIENT_ID, "Authorization": "Bearer " + helix_token})
        if response.status_code == 200:
            body = response.json()
            for stream in body["data"]:
                user = stream["user_name"]
                title = stream["title"]
                game = stream["game_name"]
                if user not in members_online:
                    if user not in expiring:
                        to_notify.append([user, title, game])
                    if user in expiring:
                        del expiring[user]
                    members_online.append(user)
                yield user
        else:
            raise


def purge_expiring():
    must_remove = time.time() - STREAM_EXPIRY
    to_remove = []
    for user, timestamp in expiring.items():
        if timestamp < must_remove:
            to_remove.append(user)
    for user in to_remove:
        del expiring[user]


def valid_twitch_user(username):
    return re.match(r"^(#)?[a-zA-Z0-9][\w]{2,24}$", username) is not None


async def perform_check():
    purge_expiring()
    helix_token = login()
    channel = client.get_channel(CHANNEL_ID)
    if not helix_token:
        sys.stderr.write("Couldn't login to Twitch Helix API!!! Waiting 1 minute before retrying")
        await asyncio.sleep(60)
    try:
        global members_online
        while True:
            to_notify = []
            found = list(check_on_twitch(set(filter(lambda x: valid_twitch_user(x), all_members.values())), helix_token, to_notify))
            for lst in to_notify:
                user, title, game = lst
                await channel.send(MESSAGE % (user, title, game, "https://twitch.tv/" + user))
            for stream in members_online:
                if stream not in found:
                    members_online.remove(stream)
                    expiring[stream] = time.time()
            with open("alive.json", "w") as f:
                json.dump(members_online, f)
            await asyncio.sleep(INTERVAL)
    except Exception:
        sys.stderr.write("Something in the checks failed! Waiting 1 minute before retrying")
        await asyncio.sleep(60)


def has_role(member):
    for role in member.roles:
        if role.id in ROLE_IDS:
            return True
    return False


def is_admin(member):
    if member.id in ADMIN_USERS:
        return True
    for role in member.roles:
        if role.id in ADMIN_IDS:
            return True
    return False


def channel_exists(channel) -> bool:
    helix_token = login()
    if not helix_token:
        raise
    response = requests.get("https://api.twitch.tv/helix/users?login=" + quote(channel), headers={"Client-ID": HELIX_CLIENT_ID, "Authorization": "Bearer " + helix_token})
    if response.status_code == 200:
        return len(response.json()["data"]) > 0


@client.event
async def on_message(message):
    try:
        global all_members
        global members_online
        channel = message.channel
        if message.content.startswith("!addstream"):
            stream = message.content.replace("!addstream ", "").replace("http://", "").replace("www.", "").replace("twitch.tv/", "").replace("/", "").strip()
            if len(stream) < 2:
                await channel.send(message.author.display_name + ", please tell me which is your stream! !addstream your_stream_name\nType !rolelive for help.")
                return
            if not valid_twitch_user(stream):
                await channel.send("Sorry " + message.author.display_name + ", I didn't understand that channel name. You must type your Twitch username without the URL (e.g. MyStream), type !rolelive for help.")
                return
            if not has_role(message.author) and not IGNORE_ROLES:
                await channel.send("Sorry " + message.author.display_name +
                                   ", your role is not authorized to add streams to the live channel. You must have one of these roles: {roles}\nType !rolelive for help."
                                   .format(roles=", ".join(ROLE_NAMES)))
                return
            try:
                if not channel_exists(stream):
                    await channel.send("It seems like " + channel + " is not an existing Twitch channel. Did you type the name correctly? Type !rolelive for help.")
            except:
                # okay, what a shame, let's add it ignoring the error
                pass
            await add_stream_of_user(all_members, channel, stream, message.author.id, message.author.display_name)
        elif message.content.startswith("!removestream"):
            if message.author.id not in all_members:
                await channel.send("Sorry " + message.author.display_name + ", you don't have any stream configured in this bot\nType !rolelive for help.")
                return
            else:
                await remove_stream_of_user(all_members, channel, message)
        elif message.content.startswith("!onlinestreams"):
            await show_streams_online(channel, members_online)
        elif message.content.startswith("!admin"):
            if not is_admin(message.author):
                await channel.send("Sorry " + message.author.display_name + ", you must be administrator to manage streamer list")
                return
            cmd = message.content.replace("!admin.", "")
            if cmd.startswith("add"):
                if "twitch.tv" in message.content:
                    await channel.send("Sorry " + message.author.display_name + ", you should add your stream name without the twitch.tv/ URL.")
                    return
                await admin_add(all_members, channel, cmd, message)
            elif cmd.startswith("remove"):
                await admin_remove(all_members, channel, cmd, message)
            elif cmd.startswith("list"):
                await channel.send("This are all the streams I know: " + ", ".join(all_members.values()))
            elif cmd.startswith("help"):
                await channel.send("Admin help:\nAdd a stream with !admin.add stream_name\nRemove a stream with !admin.remove stream_name\nList all streams with !admin.list.")
            elif cmd.startswith("reload"):
                await reload_list(channel)
        elif message.content.startswith("!rolelive"):
            await rolelive_help(channel)
    except Exception:
        pass


async def rolelive_help(channel):
    message = "**RoleLive Help** (RoleLive version " + VERSION + " by Marquii)\n```"
    message = message + "This bot keeps track of Twitch streams and notifies in channel #" + channel.name + " when users go live.\n"
    message = message + "To add yourself to this bot, make sure you have one of the following roles: " + ", ".join(
        ROLE_NAMES) + "\n"
    message = message + "Then type '!addstream stream_name'. Do not type the twitch.tv side of the URL, just the " \
                        "stream name.\n "
    message = message + "For example, if your channel is <twitch.tv/FooBar>, type '!addstream FooBar'.\n"
    message = message + "If you want to update your stream name, just type !addstream again.\n"
    message = message + "To remove your stream from the bot, type !removestream.\n"
    message = message + "You can check online channels by typing !onlinestreams.\n"
    message = message + "If you're a server administrator, type !admin.help for a list of admin commands.\n"
    message = message + "```\nPsst! Want this in your server? Visit <https://github.com/marcsances/rolelive>."
    await channel.send(message)

async def add_stream_of_user(all_members, channel, stream, author_id, author_name):
    all_members[author_id] = stream
    with open("members.json", "w") as f:
        json.dump(all_members, f)
    await channel.send("OK " + author_name + ", I added your stream " + stream + " to the list. Watch out: If you already had a stream in the list, it will be replaced with this one!")
    await update_status()


async def remove_stream_of_user(all_members, channel, message):
    del all_members[message.author.id]
    with open("members.json", "w") as f:
        json.dump(all_members, f)
    await channel.send("OK " + message.author.display_name + ", I'll no longer track your stream.")
    await update_status()


async def show_streams_online(channel, members_online):
    msg = "Streams currently online:\n"
    for stream in members_online:
        msg = msg + stream + " - <https://twitch.tv/" + stream + ">\n"
    await channel.send(msg)



async def admin_add(all_members, channel, cmd, message):
    all_members[str(uuid.uuid4())] = cmd.replace("add ", "")
    with open("members.json", "w") as f:
        json.dump(all_members, f)
    await channel.send("OK " + message.author.display_name + ", I added that stream to the list")
    await reload_list(channel)
    await update_status()


async def admin_remove(all_members, channel, cmd, message):
    target = cmd.replace("remove ", "")
    keys = map(lambda x: x[0], filter(lambda x: x[1] == target, all_members.items()))
    for key in list(keys)[:]:
        del all_members[key]
    with open("members.json", "w") as f:
        json.dump(all_members, f)
    await channel.send("OK " + message.author.display_name + ", I've removed that stream from the list")
    await update_status()


async def reload_list(channel):
    global all_members, members_online
    try:
        with open("members.json", "r") as f:
            all_members = json.load(f)
    except:
        all_members = dict()
    try:
        with open("alive.json", "r") as f:
            members_online = json.load(f)
    except:
        members_online = list()
    await channel.send("Reloaded streamer list")
    await update_status()


async def update_status():
    await client.change_presence(activity=discord.Game("!rolelive - Watching " + str(len(all_members)) + " streams"))


@client.event
async def on_ready():
    global all_members
    global members_online
    try:
        with open("members.json", "r") as f:
            all_members = json.load(f)
    except:
        all_members = dict()
    try:
        with open("alive.json", "r") as f:
            members_online = json.load(f)
    except:
        members_online = list()
    client.loop.create_task(perform_check())
    await update_status()
    print("Ready")


client.run(DISCORD_TOKEN)
