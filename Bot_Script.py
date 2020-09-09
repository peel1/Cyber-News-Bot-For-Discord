
import feedparser
import discord.ext
from discord.ext import commands
import asyncio


SetChan = int(0)
CurrentChan = str(" ")
pentry = str(" ")
ToPost = []
TOKEN = "Token"
x = int(0)

bot = commands.Bot(command_prefix='@')

@bot.command(name='set-channel', help='Sets channel to display news. USAGE: @set-channel NAME')
async def channel_set(ctx, Channel):
    global CurrentChan
    global ToPost
    id = ctx.message.guild.id
    Guild = bot.get_guild(id)
    Temp = discord.utils.get(Guild.text_channels, name=Channel)
    ID = Temp.id
    CurrentChan = bot.get_channel(ID)
    ToPost.append(CurrentChan)
    print(ID)
    global SetChan
    SetChan = int(1)
    response = ("The channel is set to {}".format(Channel))
    await ctx.send(response)

@bot.command(name='remove-channel', help='Remove channel to use. USAGE: @remove-channel NAME ')
async def channel_set(ctx, Channel):
    global ToPost
    Temp = discord.utils.get(bot.get_all_channels(), name=Channel)
    ID = Temp.id
    CuC = bot.get_channel(ID)
    ToPost.remove(CuC)
    await ctx.send("Removed Channel: {}".format(Channel))

async def status_task():
    while True:
        while SetChan == 0:
            await asyncio.sleep(20)
        global pentry
        global x
        print("Works?")
        NewsFeed = feedparser.parse("https://threatpost.com/feed/")
        entry = NewsFeed.entries[0]
        while entry == pentry:
            await asyncio.sleep(60)
            print("x")
            NewsFeed = feedparser.parse("https://threatpost.com/feed/")
            entry = NewsFeed.entries[0]
            print(entry)
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
        print(CurrentChan)
        for i in ToPost:
            TempChan = ToPost[x]
            await TempChan.send(embed=LatestNews)
            x = x + 1
        print("Posted?")
        x = int(0)
        await asyncio.sleep(60)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="The Latest Cyber News"))



bot.loop.create_task(status_task())
bot.run(TOKEN)
