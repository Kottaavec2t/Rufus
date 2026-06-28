import discord
import datetime

def make_base_embed(color: discord.Color = None):
    embed = discord.Embed()
    embed.set_footer(text="© Rufus • @kottaavec2t")
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

def get_gd_embed():
    embed = make_base_embed(discord.Color.yellow())
    embed.set_author(name="Geomtry Dash", icon_url="attachment://gd.png")
    file = discord.File("./img/logo/gd.png")
    embed.timestamp = datetime.datetime.now()
    return embed, file

def make_error_embed(error: Exception = None):
    embed = make_base_embed(discord.Color.red())
    embed.title = 'Error'
    if hasattr(error, 'message'):
        embed.add_field(name='', value=f'{str(error.message)}')
    else:
        embed.add_field(name='', value=f'{str(error)}')
    embed.timestamp = datetime.datetime.now()
    return embed