import discord
import datetime
from discord.ext import commands
import os

import SECRETS

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', intents=intents)

intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

@bot.event
async def on_ready():
	print(f"{bot.user.name} is online :")
	print("> Username :", bot.user.name)
	print("> User ID :", bot.user.id)
	print("> Date :", datetime.datetime.now())
	
	await bot.load_extension(f'cogs.minecraft_commands')
	await bot.load_extension(f'cogs.roblox_commands')
	await bot.load_extension(f'cogs.osu_commands')
	'''for filename in os.listdir("./cogs"):
		if filename.endswith(".py"):
			if filename[:-3] not in ["view"]:
				await bot.load_extension(f"cogs.{filename[:-3]}")'''

	try:
		synced = await bot.tree.sync()
		print(f"> Synced {len(synced)} commands")

	except Exception as e:
		print(e)

#Token
bot.run(SECRETS.DISCORD_API_KEY)
