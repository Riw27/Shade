import os
import sys
import json
import plyer
import psutil
import ctypes
import asyncio
import discord
import datetime
import requests
import pyautogui
from ctypes import wintypes
from discord.ext import commands

with open(file=f'{os.path.expanduser(path="~")}\AppData\Roaming\.Shade\config.json', mode='r', encoding='utf-8') as file:
    data=dict(json.load(fp=file))

client = commands.Bot(command_prefix=data.setdefault('prefix', '.'), intents=discord.Intents.all(), self_bot=True)
client.remove_command('help')

@client.event
async def on_ready():
    plyer.notification.notify(title='Бот успешно запущен', message=f'{client.user} | {client.user.id}', timeout=20)
    while True:
        await asyncio.sleep(10)
        pid=wintypes.DWORD()
        active=ctypes.windll.user32.GetForegroundWindow()
        ctypes.windll.user32.GetWindowThreadProcessId(active, ctypes.byref(pid))
        pid=pid.value
        for item in psutil.process_iter():
            if pid == item.pid:
                try:
                    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, application_id=data.setdefault('activity', {}).setdefault('application id', 1026506204438073425), name=str(item.name()[:-4]), details=str(item.name()[:-4]), assets={'large_image': str(data.setdefault('activity', {}).setdefault('asset id', 1026562828821348422)), 'large_text':f'Прошло: {str((datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(item.create_time())))[:-7]}'}, url='https://www.twitch.tv/404%27'))
                except:
                    pass

@client.command(name='ping')
async def __ping(ctx):
    try:
        await ctx.message.edit(content=f'ping **{round(1000 * client.latency)}**')
    except:
        try:
            await ctx.message.add_reaction('❌')
        except:
            pass
    else:
        try:
            await ctx.message.add_reaction('✅')
        except:
            pass

@client.command(name='delme')
async def __delme(ctx, limit:int=None, user:int=None):
    try:
        if user is None:
            async for message in ctx.message.channel.history(limit=limit):
                if message.author.id == client.user.id and message.id != ctx.message.id:
                    try:
                        await message.delete()
                    except:
                        pass
                    else:
                        await asyncio.sleep(1.5)
        elif user is not None and user == 0:
            for friend in client.user.friends:
                async for message in friend.history(limit=None):
                    if message.author.id == client.user.id and message.id != ctx.message.id:
                        try:
                            await message.delete()
                        except:
                            pass
                        else:
                            await asyncio.sleep(1.5)
        elif user is not None:
            user=await client.fetch_user(user)
            async for message in user.history(limit=limit):
                if message.author.id == client.user.id and message.id != ctx.message.id:
                    try:
                        await message.delete()
                    except:
                        pass
                    else:
                        await asyncio.sleep(1.5)
        
    except:
        try:
            await ctx.message.add_reaction('❌')
        except:
            pass
    else:
        try:
            await ctx.message.add_reaction('✅')
        except:
            pass

@client.command(name='editme')
async def __editme(ctx, limit:int, *, content):
    try:
        async for message in ctx.message.channel.history(limit=limit):
            if message.author.id == client.user.id and message.id != ctx.message.id and message.content != '':
                try:
                    await message.edit(content=content)
                except:
                    pass
                else:
                    await asyncio.sleep(1.5)
    except:
        try:
            await ctx.message.add_reaction('❌')
        except:
            pass
    else:
        try:
            await ctx.message.add_reaction('✅')
        except:
            pass

@client.command(name='ban')
async def __ban(ctx, id:int, reason=None):
    try:
        user=await client.fetch_user(id)
        await ctx.guild.ban(user=user, reason=reason)
    except:
        try:
            await ctx.message.add_reaction('❌')
        except:
            pass
    else:
        try:
            await ctx.message.add_reaction('✅')
        except:
            pass

@client.command(name='slowmode')
async def __slowmode(ctx, value:int=1):
    try:
        await ctx.channel.edit(slowmode_delay=value)
    except:
        try:
            await ctx.message.add_reaction('❌')
        except:
            pass
    else:
        try:
            await ctx.message.add_reaction('✅')
        except:
            pass

@client.command(name='user')
async def __user(ctx, id:int):
    try:
        user=await client.fetch_user(id)
        url=''
        if user.bot:
            url=f'https://discord.com/api/oauth2/authorize?client_id={user.id}&permissions=8&scope=bot%20applications.commands'
        await ctx.message.edit(content=f'> {user}\n> {user.id}\n> {user.created_at}\n\n{user.avatar_url}\n\n{url}')
    except:
        try:
            await ctx.message.add_reaction('❌')
        except:
            pass
    else:
        try:
            await ctx.message.add_reaction('✅')
        except:
            pass

@client.command(name='copy')
async def __copy(ctx):
    if not ctx.guild.id:
        return

    try:
        icon=requests.get(ctx.guild.icon_url).content
        guild=await client.create_guild(name=f'{ctx.guild.name} ?', icon=icon)
        await asyncio.sleep(5)
        guild=client.get_guild(guild.id)
        
        for channel in guild.channels:
            try: 
                await channel.delete()
            except:
                pass

        for role in ctx.guild.roles[::-1]:
            if role.name != '@everyone':
                try: 
                    await guild.create_role(name=role.name, color=role.color, permissions=role.permissions, hoist=role.hoist, mentionable=role.mentionable)
                except: 
                    pass

        for category in ctx.guild.categories:
            try: 
                await guild.create_category(name=category.name, position=category.position, overwrites=category.overwrites)
            except: 
                pass

        for channel in ctx.guild.text_channels:
            if channel.category is None:
                await guild.create_text_channel(name=channel.name, topic=channel.topic, nsfw=channel.nsfw, slowmode_delay=channel.slowmode_delay, position=channel.position, overwrite=channel.overwrites)
            else:
                category = discord.utils.get(guild.categories, name=channel.category.name)
                await guild.create_text_channel(name=channel.name, topic=channel.topic, nsfw=channel.nsfw, slowmode_delay=channel.slowmode_delay, position=channel.position, category=category, overwrites=channel.overwrites)
        for channel in ctx.guild.voice_channels:
            if channel.category is None:
                await guild.create_voice_channel(name=channel.name, position=channel.position, overwrites=channel.overwrites)
            else:
                category = discord.utils.get(guild.categories, name=channel.category.name)
                await guild.create_voice_channel(name=channel.name, positiob=channel.position, overwrites=channel.overwrites, category=category)
    except:
        try:
            await ctx.message.add_reaction('❌')
        except:
            pass
    else:
        try:
            await ctx.message.add_reaction('✅')
        except:
            pass

@client.command(name='stop')
async def __restart(ctx):
    try:
        os.abort()
    except:
        try:
            await ctx.message.add_reaction('❌')
        except:
            pass

@client.command(name='typing')
async def __typing(ctx, time:int):
    try:
        async with ctx.typing():
            await asyncio.sleep(time)
    except:
        try:
            await ctx.message.add_reaction('❌')
        except:
            pass
    else:
        try:
            await ctx.message.add_reaction('✅')
        except:
            pass

@client.command(name='/screenshot')
async def __screenshot(ctx):
    try:
        pyautogui.screenshot('screenshot.png')
        await ctx.send(file=discord.File('screenshot.png'))
        os.remove('screenshot.png')
    except:
        try:
            await ctx.message.add_reaction('❌')
        except:
            pass
    else:
        try:
            await ctx.message.add_reaction('✅')
        except:
            pass

@client.command(name='/cmd')
async def __cmd(ctx, *, body):
    try:
        os.system(body)
    except:
        try:
            await ctx.message.add_reaction('❌')
        except:
            pass
    else:
        try:
            await ctx.message.add_reaction('✅')
        except:
            pass
