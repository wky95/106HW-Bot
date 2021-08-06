import os
from discord.ext import commands
import discord
import lookupHW
import asyncio
import keep_alive
from replit import db

bot = commands.Bot(command_prefix=']')

def getHW():
    return lookupHW.HW()

@bot.event
async def on_ready():
    while True:
        try:
            x = getHW()
        except:
            await asyncio.sleep(25)
            continue
        try:
            print(x)
            Embed = discord.Embed(title=x[2], color=13704991, description=x[0])
            Embed.set_author(name=x[1])
            Embed.set_footer(text="如有任何問題請聯繫伺服器維護員")
            try:
                if x != ['', '', ''] and db[(str)(x[1]+x[2])][0]!=x[0]:
                    channel = bot.get_channel((int)(os.environ.get("CHANNEL")))
                    message = await channel.fetch_message(db[(str)(x[1]+x[2])][1])
                    await message.edit(embed=Embed)
                    db[(str)(x[1]+x[2])] = (x[0],message.id)
            except KeyError:
                if x != ['', '', '']:
                    channel = bot.get_channel((int)(os.environ.get("CHANNEL")))
                    message = await channel.send(embed=Embed)
                    db[(str)(x[1]+x[2])] = (x[0],message.id)
        except:
            pass
        await asyncio.sleep(25)
keep_alive.keep_alive()
bot.run(os.environ['TOKEN'])