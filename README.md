# rolelive
This is a very quickly hacked together Discord bot that monitors when a user with a certain role goes live on Twitch/Youtube and makes a notification on the given Discord channel.

Monitoring is done using Discord Rich Presence, so the user must have connected the Twitch account and have the streaming status public on his account.

This implementation is absolutely basic. But it may serve you as a template for a more rich bot. Up to you.

## Requirements

Linux or Mac with Python 3 and pip.

## Installation

Just install the project requirements.

```
python3 -m pip install -r -requirements.txt
```

## Configuration

Go to [Discord developer portal](https://discord.com/developers/applications), create an application. The new application has a "Client ID". Keep this information.

Go to the "Bot" tab of your new application and click on "Add Bot". Copy the "token". That is your ``CLIENT_SECRET``. Keep it (and keep it secret).

Let's make the bot join your server. Modify YOUR_CLIENT_ID with the Client ID you copied from the first step, then copy the resulting URL and visit it in your browser to add the bot to your own server:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=3072
```

Now enable Developer Mode on Discord (go to Appearance > Developer mode). This will let you get the IDs we need for the bot.

Now open the start.sh file in this project and modify the export lines with the following values:

* ``CLIENT_SECRET``: the client secret you just copied from the developer portal.
* ``GUILD_ID``: the server ID on Discord. Right click the icon of your server and click on "Copy ID".
* ``ROLE_IDS``: all the role IDs (find a user with the role, right click the role label and choose "Copy ID") for which streaming status is monitored. Each role separated by commas.
* ``CHANNEL_ID``: the ID of the channel where the live notifications will be sent. Right click the channel name to click on Copy ID.

Finally, we need to change crontab so the bot will run periodically. On a terminal, run:

```
crontab -e
```

A visual editor appears, add a line at the end of your crontab like this, changing the path ``/home/ubuntu/bots/rolelive/`` with the FULL path to where your bot code is:

```
*/5 * * * *    cd /home/ubuntu/bots/rolelive/ && ./start.sh
```

``*/5`` means the bot will run every 5 minutes. ``*/10`` would run every 10 minutes.

**Do not run the bot every minute!** You'll get a nice message from Discord telling it's connected so many times and that they changed its token. Run at least every 5 minutes, or more.

Quit the editor saving the changes. The bot will run from now on.

## Modifying the greeting message

Just modify at the ``rolelive.py`` file the ``MESSAGE`` variable. Please notice it takes three values with %s, the first is the user name, the second is the platform and the last is the link to the stream. Keep that syntax or expect errors.