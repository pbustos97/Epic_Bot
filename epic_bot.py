#!/usr/bin/python
import sys
import string
import asyncio
import discord
import numpy as np
from discord.ext import commands
from epic_bot_id import epic_bot_token
from epic_bot_default_cmds import *

# changed description
bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description='User Command Bot')

# Needed in case server does not have a .npy file yet
botDictBase = np.load('botDict.npy').item()

@bot.event
async def on_message(message):

    serverId = str(message.server.id) + '.npy'

    # Does not work if np.load(serverId).item() doesn't exist
    try:
        botDict = np.load(serverId).item()
        print(serverId + ' file loaded')
    except:
        print('Server ' + serverId + ' does not have commands dictionary file yet')
        print('Creating new file for ' + serverId)
        np.save(serverId, botDictBase)
        botDict = np.load(serverId).item()

    global botPrefix
    msg = message.content.split()
    msg[0] = msg[0][len(botPrefix):] #removes the first 2 characters './'

    # Does not work if np.load(serverId).item() doesn't exist
    if msg[0] in botDict:
        await bot.send_message(message.channel, botDict.get(msg[0]).format(message))

# Add Command
    elif msg[0] == botAddCmd and msg[1] not in botDict and message.author.top_role.permissions.manage_roles:
        if (msg[1] not in botDict):
            # parse command and bot response
            newCmd = msg[1]
            botResponse = ''
            for i in range(2,len(msg)):
                # changed order and deleted character removal
                botResponse += (msg[i] + ' ')
            print(botResponse)

            # save newCmd and botResponse to file and temp dictionary
            botDict[newCmd] = botResponse
            np.save(serverId, botDict)

        else:
            botMsg = 'Bot already has command ```' + msg[1] + '```'
            await bot.send_message(message.channel, botMsg.format(message))

# Remove Command
    elif msg[0] == botRmCmd and message.author.top_role.permissions.manage_roles:
        if msg[1] in botDict:
            del botDict[msg[1]]
            np.save(serverId, botDict)
        else:
            botMsg = 'Command not in dictionary ```' + msg[1] + '```'
            await bot.send_message(message.channel,botMsg.format(message))

# Add Role
    elif msg[0] == botAddRole:
        target = message.mentions
        if len(target) > 1:
            botMsg = '{0.author.mention}, you can edit only 1 user\'s role'
            await bot.send_message(message.channel,botMsg.format(message))
        else:
            roleList = msg[2:]
            roleStr = ''

            #Converts message list into a single string and removes whitespace on both sides
            for section in roleList:
                roleStr += section + ' '
            roleStr.strip()

            roleList = message.server.roles
            role = message.author.top_role

            # Checks if role is in the server
            for tempRole in roleList:
                if roleStr.strip() == str(tempRole.name.strip()):
                    role = tempRole
                    print(role)
                    break
                else:
                    role = None

            if role is None:
                botMsg = 'Role does not exist {0.author.mention}'
                await bot.send_message(message.channel,botMsg.format(message))

            elif message.author.top_role >= target[0].top_role:
                if role > message.author.top_role:
                    botMsg = 'Cannot assign higher role than self {0.author.mention}'
                    await bot.send_message(message.channel,botMsg.format(message))
                else:
                    await bot.add_roles(target[0],role)
                    botMsg = str(role) + ' role added to ' + target[0].mention
                    await bot.send_message(message.channel,botMsg.format(message))
            elif message.author.top_role < target[0].top_role:
                botMsg = msg[1] + ' is a superior {0.author.mention}'
                await bot.send_message(message.channel,botMsg.format(message)) 

# Remove Role
    elif msg[0] == botRmRole:
        target = message.mentions
        if len(target) > 1:
            botMsg = '{0.author.mention}, you can edit only 1 user\'s role'
            await bot.send_message(message.channel,botMsg.format(message))
        else:
            roleList = msg[2:]
            roleStr = ''

            #Converts message list into a single string and removes whitespace on both sides
            for section in roleList:
                roleStr += section + ' '
            roleStr.strip()

            roleList = message.server.roles
            role = message.author.top_role

            # Checks if role is in the server
            for tempRole in roleList:
                if roleStr.strip() == str(tempRole.name.strip()):
                    role = tempRole
                    print(role)
                    break
                else:
                    role = None
                    print('Empty')

            if role is None:
                botMsg = 'Role does not exist {0.author.mention}'
                await bot.send_message(message.channel,botMsg.format(message))

            elif message.author.top_role >= target[0].top_role:
                if role > message.author.top_role:
                    botMsg = 'Cannot remove role higher than self {0.author.mention}'
                    await bot.send_message(message.channel,botMsg.format(message))
                else:
                    await bot.remove_roles(target[0],role)
                    botMsg = str(role) + ' role removed from ' + target[0].mention
                    await bot.send_message(message.channel,botMsg.format(message))
            elif message.author.top_role < target[0].top_role:
                botMsg = msg[1] + ' is a superior {0.author.mention}'
                await bot.send_message(message.channel,botMsg.format(message))

# Ban User
    elif msg[0] == botBanCmd:
        if not message.author.top_role.permissions.ban_members:
            botMsg = '{0.author.mention} does not have permission to ban others'
            await bot.send_message(message.channel,botMsg.format(message))
        else:
            targets = message.mentions
            for target in targets:
                if target is message.author:
                    botMsg = 'Cannot ban self {0.author.mention}'
                    await bot.send_message(message.channel,botMsg.format(message))
                elif target.top_role >= message.author.top_role:
                    botMsg = 'Cannot ban peers or superiors {0.author.mention}'
                    await bot.send_message(message.channel,botMsg.format(message))
                else:
                    await bot.ban(target)

# Kick User
    elif msg[0] == botKickCmd:
        if not message.author.top_role.permissions.kick_members:
            botMsg = '{0.author.mention} does not have permission to kick others'
            await bot.send_message(message.channel,botMsg.format(message))
        else:
            targets = message.mentions
            for target in targets:
                if target is message.author:
                    botMsg = 'Cannot kick self {0.author.mention}'
                    await bot.send_message(message.channel,botMsg.format(message))
                elif target.top_role >= message.author.top_role:
                    botMsg = 'Cannot ban peers or superiors {0.author.mention}'
                    await bot.send_message(message.channel,botMsg.format(message))
                else:
                    await bot.kick(target)

    elif message.author != bot.user and message.content.startswith('./'):
        botMsg = 'Command does not exist or {0.author.mention} does not have permission'
        await bot.send_message(message.channel, botMsg.format(message))
        
@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))
    print('What is the bot prefix?')
    global botPrefix
    botPrefix = input()

bot.run(epic_bot_token)