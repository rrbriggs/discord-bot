import discord
from random import randint
from discord.ext import commands
from discord.voice_client import *

#I'm using a separate credentials file here, do what you want for that
from thunderStoleMyBabyCredentials import Credentials

TOKEN = Credentials.TOKEN
GUILD_LEADER = Credentials.GUILD_LEADER
ADMIN = Credentials.ADMIN

client = commands.Bot(command_prefix = ".")

#reporting bot name and ID in server
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

    #says hello
    if message.content.lower().startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.lower().startswith('!joke'):
        #testing joke telling
        role = ['tanking', 'healing', 'DPS']
        msg = ("Thundr's {}!".format(role[randint(0, len(role)-1)]))
        await client.send_message(message.channel, msg)

    #doesn't do much right meow
    if message.content.startswith('.help') or message.content.startswith('.?'):
        msg = ('Current available commands are: \n' 
              + '".clear x" - Where x is how many messages to clear, and can only be ran by the owner of the server'
              + '".vcmembers x" - Where x is the voice channel ID, not name'
              + '".privateToPublic" - Moves everyone from the WoW 1 - Private channel to the WoW-Public channel')
        await client.send_message(message.channel, msg)

    await client.process_commands(message)

#more safe now, checks if the user ID is my ID.
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

#report users in a voice channel
@client.command(pass_context=True)
async def vcmembers(ctx, voice_channel_id):
    # get voice channel obj
    voice_channel = discord.utils.get(ctx.message.server.channels, id = voice_channel_id)
    if not voice_channel:
        return await client.say("No voice channel found.")
    
    members = voice_channel.voice_members
    member_names = '\n'.join([x.name for x in members])

    embed = discord.Embed(title = "{} member(s) in {}".format(len(members), voice_channel.name),
                          description = member_names,
                          color=discord.Color.blue())

    return await client.say(embed = embed)

#move everyone in the WoW 1 - Private voice channel to the WoW-Public voice channel
@client.command(pass_context=True)
async def privateToPublic(ctx):

    public_voice_channel = discord.utils.get(ctx.message.server.channels, name="WoW-Public")

    voice_channel = discord.utils.get(ctx.message.server.channels, name="WoW 1 - Private")
    
    if not voice_channel:
        return await client.say("No voice channel found.")

    members = voice_channel.voice_members

    if ADMIN in [role.id for role in ctx.message.author.roles]:
        #stuff

        for member in members:
            await client.move_member(member, public_voice_channel)

    else:
        await client.say('Insufficient permissions to use privateToPublic command')

client.run(TOKEN)