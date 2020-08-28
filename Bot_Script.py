# bot.py
import os
import random
import feedparser
import discord.ext
from discord.ext import commands
from discord.ext import tasks
import asyncio

from asyncio import sleep
SetChan = int(0)
CurrentChan = str(" ")
pentry = str(" ")
TOKEN = "INSERT-TOKEN-HERE"


bot = commands.Bot(command_prefix='@')

@bot.command(name='set-channel', help='Sets channel to display news. USAGE: @set-channel NAME')
async def channel_set(ctx, Channel):
    global CurrentChan
    Temp = discord.utils.get(bot.get_all_channels(), name=Channel)
    ID = Temp.id
    CurrentChan = bot.get_channel(ID)
    print(ID)
    global SetChan
    SetChan = int(1)
    response = ("The channel is set to {}".format(Channel))
    await ctx.send(response)

async def status_task():
    while True:
        global pentry
        NewsFeed = feedparser.parse("https://threatpost.com/feed/")
        entry = NewsFeed.entries[1]
        if entry == pentry:
            break
        print(entry)
        Rtitle = entry.title
        Rdesc = entry.summary
        pentry = entry
        URL = entry.link
        LatestNews = discord.Embed(
            title=Rtitle, url= URL,
            description=Rdesc,
            color=discord.Colour(value=0xff1414),
        )
        LatestNews.set_footer(text="Cyber News Bot by peel1 - Powered by threatpost.com")
        await CurrentChan.send(embed=LatestNews)
        await sleep(10)


@bot.event
async def on_ready():
    while SetChan == 0:
        await asyncio.sleep(10)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="The Latest Cyber News"))
    bot.loop.create_task(status_task())



bot.run(TOKEN)
