import discord
from discord.ext import commands
import json

Bot = commands.Bot("fortem!", intents=discord.Intents.all())


@Bot.event
async def on_ready():
    print('Bot şuanda çalışır durumda..')


@commands.has_permissions(manage_channels=True)
@Bot.command()
async def setchannel(ctx, channelId=0):
    try:
        state = {
            "number": 0,
            "id": channelId,
            "endPerson": 0
                }
        jsonobject = json.dumps(state, indent=4)
        with open("values.json", "w") as outfile:
            outfile.write(jsonobject)
        await ctx.send(f"**{state['id']} Başarılı! Kanal ayarlandı.**")
    except:
        await ctx.send("**Hata! Kanal ayarlanamadı**")

@commands.has_permissions(manage_channels=True)
@Bot.command()
async def getchannel(ctx):
        outfile = open(f"values.json")
        f = json.load(outfile)
        await ctx.send(f'**Sayı kanalı: {f["id"]}**')

@Bot.event
async def on_message(message):

    outfile = open("values.json")
    f = json.load(outfile)
    if message.channel.id == f["id"]:
        if message.author.id != f["endPerson"]:
            if str(message.content) == str(f["number"]+1):
                await message.add_reaction("✔️")
                f["number"] += 1
                f["endPerson"] = message.author.id
                jsonobject = json.dumps(f, indent=4)
                with open("values.json", "w") as outfile:
                    outfile.write(jsonobject)
            else:
                await message.add_reaction("❌")
        else:
            await message.channel.send(f"{message.author}, sıra sende değil!")
            await message.delete()


    await Bot.process_commands (message)



Bot.run('TOKEN')
