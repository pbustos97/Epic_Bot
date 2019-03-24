#!/usr/bin/python
import sys
import string
import asyncio
import discord
import numpy as np
from discord.ext import commands
from epic_bot_id import epic_bot_token
from epic_bot_default_cmds import botAddCmd
from epic_bot_default_cmds import botRmCmd

bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description='Meme bot')

# Needed in case server does not have a .npy file yet
botDictBase = np.load('botDict.npy').item()

@bot.event
async def on_message(message):

    serverId = str(message.server.id) + '.npy'

    # does not work if np.load(serverId).item() doesn't exist
    try:
        botDict = np.load(serverId).item()
    except:
        print('Server ' + serverId + ' does not have commands dictionary file yet')
        print('Creating new file for ' + serverId)
        np.save(serverId, botDictBase)
        botDict = np.load(serverId).item()


    msg = message.content.split()
    msg[0] = msg[0][2:] #removes the first 2 characters './'

    # does not work if np.load(serverId).item() doesn't exist
    if msg[0] in botDict:
        await bot.send_message(message.channel, botDict.get(msg[0]).format(message))

    elif message.content.startswith(botAddCmd) and msg[1] not in botDict:
        if (msg[1] not in botDict):
            # parse command and bot response
            newCmd = msg[1]
            botResponse = ''
            for i in range(2,len(msg)):
                botResponse += (' ' + msg[i])
            botResponse = botResponse[1:]
            print(botResponse)

            # save newCmd and botResponse to file and temp dictionary
            botDict[newCmd] = botResponse
            np.save(serverId, botDict)

        else:
            botMsg = 'Bot already has command ```' + msg[1] + '```'
            await bot.send_message(message.channel, botMsg.format(message))

    elif message.content.startswith(botRmCmd):
        if msg[1] in botDict:
            del botDict[msg[1]]
            np.save(serverId, botDict)
        else:
            botMsg = 'Command not in dictionary ```' + msg[1] + '```'
            await bot.send_message(message.channel,botMsg.format(message))

    elif message.author != bot.user and message.content.startswith('./'):
        botMsg = 'Command does not exist'
        await bot.send_message(message.channel, botMsg.format(message))
        
@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))

bot.run(epic_bot_token)