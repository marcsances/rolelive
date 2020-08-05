import requests
import sys
import time
import discord
import datetime
from discord import Streaming
import uuid
from threading import Timer
import json
import asyncio

GUILD_ID=GUILD_ID
ROLE_IDS=[ROLE_IDS]
ADMIN_IDS=[ADMIN_IDS]
ADMIN_USERS=[ADMIN_USERS]
CLIENT_SECRET='CLIENT_SECRET'
CHANNEL_ID=CHANNEL_ID
MESSAGE="Hey guys! %s is live on %s! Check it out at %s"
TWITCH_CLIENT_ID="TWITCH_ID"
INTERVAL=30

client = discord.Client()

all_members = dict()
members_online = []

def check_on_twitch(member):
    response = requests.get("https://api.twitch.tv/kraken/users?login=" + member, headers={"Client-ID": TWITCH_CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"})
    if response.status_code == 200:
        body = response.json()
        if len(body["users"]) > 0:
            uid = body["users"][0]["_id"]
            response2 = requests.get("https://api.twitch.tv/kraken/streams/" + str(uid), headers={"Client-ID": TWITCH_CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"})
            if response2.status_code == 200:
                body2 = response2.json()
                if body2["stream"] != None:
                    return True
    return False

async def perform_check():
    global members_online
    while True:
        found = []
        for stream in set(all_members.values()):
            if check_on_twitch(stream):
                if stream not in members_online:
                    members_online.append(stream)
                    channel = client.get_channel(CHANNEL_ID)
                    await channel.send(MESSAGE % (stream, "Twitch", "https://twitch.tv/" + stream))
                found.append(stream)
            await asyncio.sleep(2)
        for stream in members_online:
            if stream not in found:
                members_online.remove(stream)
        with open("alive.json", "w") as f:
            json.dump(members_online, f)
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
    global all_members
    global members_online
    channel = message.channel
    if message.content.startswith("!addstream"):
        if len(message.content) < 14:
            await channel.send(message.author.name + ", please tell me which is your stream! !addstream your_stream_name")
            return
        if "twitch.tv/" in message.content:
            await channel.send("Sorry " + message.author.name + ", you should add your stream name without the twitch.tv/ URL.")
            return
        if not has_role(message.author):
            await channel.send("Sorry " + message.author.name + ", your role is not authorized to add streams to the live channel. You must be of either DJ or Producer role.")
            return
        all_members[message.author.id] = message.content.replace("!addstream ", "")
        with open("members.json", "w") as f:
            json.dump(all_members, f)
        await channel.send("OK " + message.author.name + ", I added your stream to the list")
    elif message.content.startswith("!removestream"):
        if message.author.id not in all_members:
            await channel.send("Sorry " + message.author.name + ", you don't have any stream configured in this bot")
            return
        else:
            del all_members[message.author.id]
            with open("members.json", "w") as f:
                json.dump(all_members, f)
            await channel.send("OK " + message.author.name + ", I'll no longer track your stream.")
    elif message.content.startswith("!onlinestreams"):
        msg = "Streams currently online:\n"
        for stream in members_online:
            msg = msg + stream + " - <https://twitch.tv/" + stream + ">\n"
        await channel.send(msg)
    elif message.content.startswith("!admin"):
        if not is_admin(message.author):
            await channel.send("Sorry " + message.author.name + ", you must be administrator to manage streamer list")
            return
        cmd = message.content.replace("!admin.", "")
        if cmd.startswith("add"):
            if "twitch.tv" in message.content:
                await channel.send("Sorry " + message.author.name + ", you should add your stream name without the twitch.tv/ URL.")
                return
            all_members[str(uuid.uuid4())] = cmd.replace("add ", "")
            with open("members.json", "w") as f:
                json.dump(all_members, f)
            await channel.send("OK " + message.author.name + ", I added that stream to the list")
        elif cmd.startswith("remove"):
            target = cmd.replace("remove ", "")
            keys = map(lambda x: x[0], filter(lambda x: x[1] == target, all_members.items()))
            for key in list(keys)[:]:
                del all_members[key]
            with open("members.json", "w") as f:
                json.dump(all_members, f)
            await channel.send("OK " + message.author.name + ", I've removed that stream from the list")
        elif cmd.startswith("list"):
            await channel.send("This are all the streams I know: " + ", ".join(all_members.values()))
        elif cmd.startswith("help"):
            await channel.send("Admin help:\nAdd a stream with !admin.add stream_name\nRemove a stream with !admin.remove stream_name\nList all streams with !admin.list.")
        elif cmd.startswith("reload"):
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
    print("Ready")


client.run(CLIENT_SECRET)

# bot invite url: https://discord.com/oauth2/authorize?client_id=736694316059328594&scope=bot&permissions=3072
