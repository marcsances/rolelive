import asyncio
import json
import re
import sys
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict

import discord
import requests

print("Please replace all client IDs, role IDs and tokens with the configuration you want for your server before "
      "using Rolelive for the first time, then remove this print and the inmediately following line.")
sys.exit(1)

# Twitch Client ID for the bot to query the API
TWITCH_CLIENT_ID = "REPLACE_ME"
# Polling interval
INTERVAL = 10
# Names of the roles
ROLE_NAMES = ["Test User", "Test Admin"]
# Message to show when somebody is live
MESSAGE = "%s is now live: **%s** - _%s_ - %s"
# RoleLive version
VERSION = "0.3.1"
# Discord Server ID that RoleLive will join
GUILD_ID = REPLACE_ME
# Discord valid role IDs
ROLE_IDS = [REPLACE_ME, REPLACE_ME]
# Discord admin role IDs
ADMIN_IDS = [REPLACE_ME]
# Discord admin user IDs
ADMIN_USERS = [REPLACE_ME]
# Discord bot token
CLIENT_SECRET = 'REPLACE_ME'
# Discord notification channel ID
CHANNEL_ID = REPLACE_ME
# Time that must pass since a channel goes offline to be considered elligible for notifications again
# This prevents duplicate notifications for when a channel has technical issues
STREAM_EXPIRY = 3600
# Ignore role IDs and let anyone add their streams with no restrictions
IGNORE_ROLES = False


class ChannelStatus(Enum):
    ONLINE = 0
    OFFLINE = 1


class Member:
    def __init__(self, channel, status):
        self.channel = channel
        self.status = status
        self.last_seen = datetime.now()


channel_name = ""
client = discord.Client()
all_members = dict()
members_online: Dict[str, Member] = dict()


def check_on_twitch(member):
    try:
        response = requests.get("https://api.twitch.tv/kraken/users?login=" + member,
                                headers={"Client-ID": TWITCH_CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"})
        if response.status_code == 200:
            body = response.json()
            if len(body["users"]) > 0:
                uid = body["users"][0]["_id"]
                response2 = requests.get("https://api.twitch.tv/kraken/streams/" + str(uid),
                                         headers={"Client-ID": TWITCH_CLIENT_ID,
                                                  "Accept": "application/vnd.twitchtv.v5+json"})
                if response2.status_code == 200:
                    body2 = response2.json()
                    if body2["stream"] != None:
                        return body2
    except Exception:
        return "Error"
    return None


async def perform_check():
    global members_online
    while True:
        try:
            found = []
            for stream in set(all_members.values()):
                print("Checking status for " + stream)
                stream_info = check_on_twitch(stream)
                if stream_info is not None:
                    if stream not in members_online and stream_info != "Error":
                        print(stream + " is online")
                        members_online[stream] = Member(stream, ChannelStatus.ONLINE)
                        channel = client.get_channel(CHANNEL_ID)
                        title = stream_info["stream"]["channel"]["status"]
                        game = stream_info["stream"]["channel"]["game"]
                        await channel.send(MESSAGE % (stream, title, game, "https://twitch.tv/" + stream))
                    found.append(stream)
                await asyncio.sleep(2)
            for stream in members_online:
                if stream not in found:
                    stream.status = ChannelStatus.OFFLINE
                    if (datetime.now() - stream.last_seen).total_seconds() > STREAM_EXPIRY:
                        del members_online[stream]
                else:
                    stream.status = ChannelStatus.ONLINE
                    stream.last_seen = datetime.now()
            with open("channel_status.json", "w") as f:
                json.dump(members_online, f)
        except Exception as e:
            pass
        finally:
            await asyncio.sleep(INTERVAL)


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


@client.event
async def on_message(message):
    try:
        global all_members
        global members_online
        channel = message.channel
        if message.content.startswith("!addstream"):
            if len(message.content) < 14:
                await channel.send(
                    message.author.display_name + ", please tell me which is your stream! !addstream "
                                                  "your_stream_name\nType !rolelive for help.")
                return
            if not has_role(message.author) and not IGNORE_ROLES:
                await channel.send("Sorry " + message.author.display_name +
                                   ", your role is not authorized to add streams to the live channel. You must have "
                                   "one of these roles: {roles}\nType !rolelive for help. "
                                   .format(roles=", ".join(ROLE_NAMES)))
                return
            await add_stream_of_user(all_members, channel, message)
        elif message.content.startswith("!removestream"):
            if message.author.id not in all_members:
                await channel.send(
                    "Sorry " + message.author.display_name + ", you don't have any stream configured in this "
                                                             "bot\nType !rolelive for help.")
                return
            else:
                await remove_stream_of_user(all_members, channel, message)
        elif message.content.startswith("!onlinestreams"):
            await show_streams_online(channel, members_online)
        elif message.content.startswith("!streaminfo"):
            await show_stream_info(channel, message)
        elif message.content.startswith("!admin"):
            if not is_admin(message.author):
                await channel.send(
                    "Sorry " + message.author.display_name + ", you must be administrator to manage streamer list")
                return
            cmd = message.content.replace("!admin.", "")
            if cmd.startswith("add"):
                if "twitch.tv" in message.content:
                    await channel.send(
                        "Sorry " + message.author.display_name + ", you should add your stream name without the "
                                                                 "twitch.tv/ URL.")
                    return
                await admin_add(all_members, channel, cmd, message)
            elif cmd.startswith("remove"):
                await admin_remove(all_members, channel, cmd, message)
            elif cmd.startswith("list"):
                await channel.send("This are all the streams I know: " + ", ".join(all_members.values()))
            elif cmd.startswith("help"):
                await channel.send(
                    "Admin help:\nAdd a stream with !admin.add stream_name\nRemove a stream with !admin.remove "
                    "stream_name\nList all streams with !admin.list.")
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


async def add_stream_of_user(all_members, channel, message):
    try:
        stream = re.search(r'(?:(?:https?://)?(?:www\.)?twitch\.tv/)?([a-zA-Z0-9][\w]{2,24}$)',
                           message.content.replace("!addstream ", "").strip(), re.IGNORECASE).group(1)
    except AttributeError:
        await channel.send("Sorry " + message.author.display_name + ", I couldn't guess your stream from your "
                                                                    "message. Could you please type your Twitch "
                                                                    "username without the URL?")
        return
    all_members[message.author.id] = stream
    with open("members.json", "w") as f:
        json.dump(all_members, f)
    await channel.send(
        "OK " + message.author.display_name + ", your stream " + stream + " has been added to the list. Please ensure "
                                                                          "I got the name right. Notice that if you "
                                                                          "already had an stream in the list, "
                                                                          "it has been replaced.")
    await update_status()


async def remove_stream_of_user(all_members, channel, message):
    del all_members[message.author.id]
    with open("members.json", "w") as f:
        json.dump(all_members, f)
    await channel.send("OK " + message.author.display_name + ", I'll no longer track your stream.")
    await update_status()


async def show_streams_online(channel, members_online):
    msg = "Streams currently online:\n"
    for stream in map(lambda s: s.channel, filter(lambda x: x.status == ChannelStatus.ONLINE, members_online.values())):
        msg = msg + stream + " - <https://twitch.tv/" + stream + ">\n"
    msg = msg + "Type !streaminfo <stream_name> to get more information for a certain stream"
    await channel.send(msg)


async def show_stream_info(channel, message):
    user = message.content.replace("!streaminfo ", "")
    stream_info = check_on_twitch(user)
    if stream_info is not None:
        game = stream_info["stream"]["channel"]["game"]
        title = stream_info["stream"]["channel"]["status"]
        viewers = stream_info["stream"]["viewers"]
        link = "https://twitch.tv/" + user
        message = "{user} is live playing {game}\n{title}\n{viewers} viewers\nWatch on {link}".format(user=user,
                                                                                                      game=game,
                                                                                                      title=title,
                                                                                                      viewers=viewers,
                                                                                                      link=link)
        await channel.send(message)
    else:
        await channel.send("This stream seems to be offline or may not exist.")


async def admin_add(all_members, channel, cmd, message):
    all_members[str(uuid.uuid4())] = cmd.replace("add ", "")
    with open("members.json", "w") as f:
        json.dump(all_members, f)
    await channel.send("OK " + message.author.display_name + ", I added that stream to the list")
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
        with open("channel_status.json", "r") as f:
            members_online = json.load(f)
    except:
        members_online = dict()
    await channel.send("Reloaded streamer list")
    await update_status()


async def update_status():
    await client.change_presence(activity=discord.Game("!rolelive - Watching " + str(len(all_members)) + " streams"))


@client.event
async def on_ready():
    global all_members
    global members_online
    global channel_name
    channel_name = client.get_channel(CHANNEL_ID)
    try:
        with open("members.json", "r") as f:
            all_members = json.load(f)
    except:
        all_members = dict()
    try:
        with open("channel_status.json", "r") as f:
            members_online = json.load(f)
    except:
        members_online = dict()
    client.loop.create_task(perform_check())
    await update_status()
    print("Ready")


client.run(CLIENT_SECRET)
