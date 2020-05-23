import discord
import random
import asyncio
import time
from discord.ext import commands
from discord.voice_client import *

# I'm using a separate credentials file here, do what you want for that
from thunderStoleMyBabyCredentials import Credentials

import WeightedUserLogic
import UserJsonLoader

TOKEN = Credentials.TOKEN
GUILD_LEADER = Credentials.GUILD_LEADER
ADMIN = Credentials.ADMIN

weighted_user_logic = WeightedUserLogic.UserWeightedMadness()
user_json_loader = UserJsonLoader.UserJsonLoader()

client = commands.Bot(command_prefix=".")

alert_on = False


# reporting bot name and ID in server
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    # Hey bot, quit talking to yourself
    if message.author == client.user:
        return

    # says hello
    if message.content.lower().startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    # Letterkenny throwback
    if "to be fair" in message.content.lower():
        msg = 'To be faaaaaaaaaair!'
        await client.send_message(message.channel, msg)
        await client.send_message(message.channel, msg)

    # joke telling
    if message.content.lower().startswith('!joke'):
        role = ['tanking', 'healing', 'DPS']
        team_member = weighted_user_logic.GetUserForJoke()

        person = "{}'s ".format(team_member)
        affliction = "{}!".format(random.choice(role))
        msg = person + affliction
        await client.send_message(message.channel, msg)

    # time
    if message.content.lower().startswith('!time'):
        localtime = time.asctime(time.localtime(time.time()))
        await client.send_message(message.channel, localtime)

    # link to github
    if message.content.lower().startswith('!source'):
        source_link = "https://github.com/rrbriggs/discord-bot"
        await client.send_message(message.channel, source_link)

    if message.content.startswith('.help') or message.content.startswith('.?'):
        msg = ('``` \n'
               + 'Current available commands are: \n'
               + 'DISCORD OWNER ONLY \n'
               + '".clear x" - Where x is how many messages to clear, and can only be ran by the owner of the server \n'
               + '".addMember x" - Add x member to the team / joke list! \n'
               + '".removeMember x" - Remove x member to the team / joke list! \n'
               + '".resetWeights" - Reset each members weight to the avg weight. \n'
               + '\n'
               + 'ALL USERS\n'
               + '".getWeights" - Return all users and their weightings \n'
               + '".vcmembers x" - Where x is the voice channel ID, not name \n'
               + '".moveRaid" - Moves everyone from the WoW 1 - Private channel to the WoW-Public channel, if additional WoWGeneral argument given, it will move from that channel instead \n'
               + '"!joke" - Tells very funny definitely not repetitive or played out jokes \n'
               + '"!source" - Links to bot github \n'
               + '"!time" - Tells time in Texas Freedom Time \n'
               + '```')
        await client.send_message(message.channel, msg)

    await client.process_commands(message)


# discord.ext.commands.errors.CommandInvokeError:
# - Command raised an exception: HTTPException: BAD REQUEST (status code: 400): You can only bulk delete messages that are under 14 days old.
# more safe now, checks if the user ID is my ID.
# clear x amount of recent messages
@client.command(pass_context=True)
async def clear(ctx, amount=5):
    if ctx.message.author.id == GUILD_LEADER:
        channel = ctx.message.channel
        messages = []
        async for message in client.logs_from(channel, limit=int(amount)):
            messages.append(message)
        await client.delete_messages(messages)
        await client.say('Messages deleted.')
    else:
        await client.say('Insufficient permissions to prerform clear operation')


# add a member to the json list of users and weights
@client.command(pass_context=True)
async def addMember(ctx, new_member):
    if ctx.message.author.id == GUILD_LEADER:
        user_json_loader.add_new_member(new_member)

        await client.say("Added {}!".format(new_member))


@client.command(pass_context=True)
async def toggle_raid_alert(ctx, raid_alert):
    global alert_on
    if ctx.message.author.id == GUILD_LEADER:

        if raid_alert == "on":
            alert_on = True
        elif raid_alert == "off":
            alert_on = False
        elif raid_alert == "status":
            if alert_on:
                await client.say("Raid Alert is ON.")
                return
            else:
                await client.say("Raid Alert is OFF.")
                return

        await client.say("Raid Alert: {}!".format(raid_alert))


# add a remove to the json list of users and weights
@client.command(pass_context=True)
async def removeMember(ctx, member):
    if ctx.message.author.id == GUILD_LEADER:
        user_json_loader.remove_user(member)

        await client.say("Removed {}!".format(member))


# reset all weights from json list
@client.command(pass_context=True)
async def resetWeights(ctx):
    if ctx.message.author.id == GUILD_LEADER:
        user_json_loader.reset_user_weights_all()

        await client.say("All weights reset!")


# get all users and weights from json list
@client.command(pass_context=True)
async def getWeights(ctx):
    await client.say(user_json_loader.get_users_and_weights())


# report users in a voice channel
@client.command(pass_context=True)
async def vcmembers(ctx, voice_channel_id):
    # get voice channel obj
    voice_channel = discord.utils.get(ctx.message.server.channels, id=voice_channel_id)
    if not voice_channel:
        return await client.say("No voice channel found.")

    members = voice_channel.voice_members
    member_names = '\n'.join([x.name for x in members])

    embed = discord.Embed(title="{} member(s) in {}".format(len(members), voice_channel.name),
                          description=member_names,
                          color=discord.Color.blue())

    return await client.say(embed=embed)


# move everyone in the WoW 1 - Private voice channel to the WoW-Public voice channel
@client.command(pass_context=True)
async def moveRaid(ctx, channel_mod="WoWPrivate"):
    public_voice_channel = discord.utils.get(ctx.message.server.channels, name="WoW-Public")

    voice_channel = discord.utils.get(ctx.message.server.channels, name="WoW 1 - Private")
    private_general = discord.utils.get(ctx.message.server.channels, name="General")

    channel_mod_and_name_dict = {
        "WoWPrivate": voice_channel,
        "WoWGeneral": private_general
    }

    if not voice_channel:
        return await client.say("No voice channel found.")

    members = channel_mod_and_name_dict[channel_mod].voice_members

    member_count = len(members)

    if ADMIN in [role.id for role in ctx.message.author.roles]:

        # this check should handle members joining the channel during the member moveing process
        while member_count > 0:

            for member in members:
                await client.move_member(member, public_voice_channel)

            member_count = len(channel_mod_and_name_dict[channel_mod].voice_members)


    else:
        await client.say('Insufficient permissions to use moveRaid command')


# time shenanigans
# sends an alert to a channel if it is a raid day and 5PM
async def raid_reminder():
    await client.wait_until_ready()

    channel = discord.Object(id=479104049325801483)
    pub_channel = discord.Object(id=517037569377173504)

    while not client.is_closed:
        tardis = datetime.datetime.now()
        if tardis.weekday() == 4 and tardis.hour == 17 and alert_on:
            await client.send_message(channel,
                                      "@everyone RAID DAY: FRIDAY - 8:30PM CST (Texas Time/Freedom Time) THIS IS 9:30 EST/peon time")
            await client.send_message(pub_channel,
                                      "@everyone RAID DAY: FRIDAY - 8:30PM CST (Texas Time/Freedom Time) THIS IS 9:30 EST/peon time")

        if tardis.weekday() == 5 and tardis.hour == 17 and alert_on:
            await client.send_message(channel,
                                      "@everyone RAID DAY: SATURDAY - 8:00PM CST (Texas Time/Freedom Time) THIS IS 9:00 EST/peon time")
            await client.send_message(pub_channel,
                                      "@everyone RAID DAY: SATURDAY - 8:00PM CST (Texas Time/Freedom Time) THIS IS 9:00 EST/peon time")

        await asyncio.sleep(1800)


client.loop.create_task(raid_reminder())
client.run(TOKEN)
