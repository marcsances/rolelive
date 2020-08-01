#!/usr/bin/env python3

import discord
from discord import Streaming
import json
import os

GUILD_ID=os.environ["GUILD_ID"]
ROLE_IDS=os.environ["ROLE_IDS"].split(",")
CLIENT_SECRET=os.environ["CLIENT_SECRET"]
CHANNEL_ID=os.environ["CHANNEL_ID"]
MESSAGE="Hey guys! %s is live on %s! Check it out at %s"

client = discord.Client()

members_online = []
members_found = []

async def check_on_twitch(member):
    global members_online
    global members_found
    if isinstance(member.activity, Streaming):
        if member.id not in members_online:
            members_online.append(member.id)
            channel = client.get_channel(CHANNEL_ID)
            msg = MESSAGE % (member.name, member.activity.platform, member.activity.url)
            await channel.send(msg)
        members_found.append(member.id)

def has_role(member):
    for role in member.roles:
        if role.id in ROLE_IDS:
            return True
    return False    


@client.event
async def on_ready():
    global members_online
    global members_found
    guild = client.get_guild(GUILD_ID)
    if guild:
        for member in filter(has_role, guild.members):
            await check_on_twitch(member)
        should_remove = []
        for member_id in members_online:
            if member_id not in members_found:
                should_remove.append(member_id)
        for member_id in should_remove:
            members_online.remove(member_id)
        with open("/tmp/online" + GUILD_ID, "w") as f:
            ob = dict()
            ob["list"] = members_online
            json.dump(ob, f)
    await client.logout()
try:
    with open("/tmp/online" + GUILD_ID, "r") as f:
        ob = json.load(f)
        members_online = ob["list"]
except:
    members_online = []

client.run(CLIENT_SECRET)
