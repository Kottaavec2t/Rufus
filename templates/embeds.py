import discord
import datetime

def make_base_embed(color: discord.Color = None):
    embed = discord.Embed()
    embed.set_footer(text="© • Rufus • @kottaavec2t")
    if color is not None:
        embed.color = color
    embed.timestamp = datetime.datetime.now()
    return embed

def get_minecraft_embed():
    embed = make_base_embed(discord.Color.green())
    embed.set_author(name="Minecraft", icon_url="attachment://minecraft.png")
    file = discord.File("./img/logo/minecraft.png")
    embed.timestamp = datetime.datetime.now()
    return embed, file

def get_roblox_embed():
    embed = make_base_embed(discord.Color.blurple())
    embed.set_author(name="Roblox", icon_url="attachment://roblox.png")
    file = discord.File("./img/logo/roblox.png")
    embed.timestamp = datetime.datetime.now()
    return embed, file

def get_osu_embed():
    embed = make_base_embed(discord.Color.pink())
    embed.set_author(name="Osu!", icon_url="attachment://osu.png")
    file = discord.File("./img/logo/osu.png")
    embed.timestamp = datetime.datetime.now()
    return embed, file

def make_error_embed(error = None):
    embed = make_base_embed(discord.Color.red())
    embed.title = 'Error'
    embed.description = '> An error has occured during the command execution.\n\n[signal this error](https://example.com/)'
    embed.add_field(name='error message', value=error)
    embed.timestamp = datetime.datetime.now()
    return embed