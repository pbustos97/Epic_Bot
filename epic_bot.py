#!/usr/bin/python
import sys
import string
import asyncio
import discord
import random
import time
import numpy as np
from discord.ext import commands
from epic_bot_id import epic_bot_token
from epic_bot_id import botDict
from epic_bot_id import botAddCmd
from epic_bot_id import botRmCmd

bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description='Meme bot')

botDict = np.load('botDict.npy').item()

@bot.event
async def on_message(message):
    msg = message.content.split()
    msg[0] = msg[0][2:] #removes the first 2 characters './'

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
            np.save('botDict.npy', botDict)

        else:
            botMsg = 'Bot already has command ```' + msg[1] + '```'
            await bot.send_message(message.channel, botMsg.format(message))

    elif message.content.startswith(botRmCmd):
        if msg[1] in botDict:
            del botDict[msg[1]]
            np.save('botDict.npy', botDict)
        else:
            botMsg = 'Command not in dictionary ```' + msg[1] + '```'
            await bot.send_message(message.channel,botMsg.format(message))

    elif message.author != bot.user:
        botMsg = 'Command does not exist'
        await bot.send_message(message.channel, botMsg.format(message))

@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))

bot.run(epic_bot_token)