# We're working on a new, exciting version with more features!

We're building a Discord server to get more feedback and give updates. Feel free to join here: https://discord.gg/XBAtC4MxKb

# rolelive

This is a very quickly hacked together Discord bot that monitors when a user with a certain role goes live on Twitch and makes a notification on the given Discord channel. Current version is rolelive2.py.

Users can add their streams using the !addstream command.

There is also an implementation using a different approach (Rich Presence) in rolelive.py. That implementation is absolutely basic. But it may serve you as a template for a more rich bot. Up to you.

## User commands

* !addstream stream_name - users can add their stream using this command, if they have an authorized role. Users may only have a stream at once, running this command with more than one stream will replace the stream.
* !removestream - users can remove the stream they've added so the bot doesn't track it.
* !onlinestreams - shows a list of live streams
* !rolelive - shows RoleLive help and version

## Admin commands

This commands require the user running them to have a role of ADMIN_IDS or be one of ADMIN_USERS.

* !admin.add stream_name - adds the given stream to watch. Notice this stream is not linked to any Discord user, you can add as many as you want.
* !admin.remove stream_name - removes the given stream from the list.
* !admin.reload - reloads the stream list from the members.json file. Useful if you're making huge offline changes like populating the list for the first time.

## Requirements

Linux or Mac with Python 3 and pip.

## Installation

Just install the project requirements.

```bash
python3 -m pip install -r -requirements.txt
```

## Docker-compose

### Using docker-compose

First install 'docker' and 'docker-compose' packages to your system.

#### Installing docker

- Debian/Ubuntu/Raspbian systems

```bash
sudo su
curl https://get.docker.com/ | bash
```

- Using Pacman

```bash
pacman -S docker
systemctl enable docker  
```

#### Installing docker-compose

This process is shared between all the distributions.

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
#### Verifying the installation

To check the packages been installed correctly run:

```bash
docker -v
docker-compose -v
```

### Configure docker-compose 

Modify the .env file located at the same folder as docker-compose with the desired values, ie:

```text
MEMCACHED_USERNAME=desired_username
MEMCACHED_PASSWORD=desired_password
```

### Running docker-compose
Move to the docker project folder and run:
```bash
cd /path/to/rolelive/folder/docker
docker-compose up
```

## Configuration

Go to [Discord developer portal](https://discord.com/developers/applications), create an application. The new application has a "Client ID". Keep this information.

Go to the "Bot" tab of your new application and click on "Add Bot". Copy the "token". That is your ``CLIENT_SECRET``. Keep it (and keep it secret).

Let's make the bot join your server. Modify YOUR_CLIENT_ID with the Client ID you copied from the first step, then copy the resulting URL and visit it in your browser to add the bot to your own server:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=3072
```

Now enable Developer Mode on Discord (go to Appearance > Developer mode). This will let you get the IDs we need for the bot.

Now open the rolelive2.py file in this project and modify the export lines with the following values:

* ``CLIENT_SECRET``: the client secret you just copied from the developer portal.
* ``GUILD_ID``: the server ID on Discord. Right click the icon of your server and click on "Copy ID".
* ``ROLE_IDS``: all the role IDs (find a user with the role, right click the role label and choose "Copy ID") authorized to add their stream. Each role separated by commas.
* ``ROLE_NAMES``: names of the roles in ROLE_IDS, for help purposes
* ``CHANNEL_ID``: the ID of the channel where the live notifications will be sent. Right click the channel name to click on Copy ID.
* ``INTERVAL``: polling rate for the bot. This interval is the time the bot will sleep after checking all streams, before starting another cycle. Allows to help with rate limiting APIs, at the cost of less responsiveness. Keep it between 0 (for a lot of streams) to 120.
* ``ADMIN_USERS``: **User IDs** allowed to manage the service.
* ``ADMIN_IDS``: **Role IDs** allowed to manage the service (i.e. ALL users with the role will be able to run admin commands).
* ``TWITCH_CLIENT_ID``: Twitch client ID required for accessing Twitch API. Get an ID [here](https://dev.twitch.tv/console/apps).

## Installation

Install as a [regular systemd service](https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6).
