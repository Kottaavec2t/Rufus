import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from io import BytesIO

from templates import embeds
from utils import minecraft_tools


class minecraftCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='minecraft-info', description='Information about a minecraft player')
    async def minecraft_info(self, interaction: discord.Interaction, username: str = None, uuid: str = None):
        if username is None and uuid is None: return

        player_profile = minecraft_tools.get_player_profile(username, uuid)

        uuid = player_profile['uuid']
        full_uuid = player_profile['full_uuid']
        username = player_profile['name']
        name_history = player_profile['name_history']
        updated_at = player_profile['updated_at']
        date = datetime.fromisoformat(str(updated_at))

        skin_image = minecraft_tools.get_player_skin_render(username, uuid)
        skin_file  = None
        with BytesIO() as image_binary:
            skin_image.save(image_binary, 'PNG')
            image_binary.seek(0)
            skin_file = discord.File(fp=image_binary, filename='image.png')

        embed, file = embeds.get_minecraft_embed()
        embed.title = f'Minecraft information'
        embed.add_field(
            name=f'{username} profile',
            value=
            f'> **Username:** `{username}`'
            f'\n> **UUID:** `{uuid}`',
            inline=True
        )
        embed.set_thumbnail(
            url='attachment://image.png'
        )
        name_history_str = ''
        for i, name in enumerate(name_history):
            name_history_str += f'> **{i+1}.** `{name['name']}` {'(current)' if name['active'] else ''} {f'*{datetime.fromisoformat(name['changed_at']).strftime("%d/%m/%Y, %H:%M:%S")}*' if name['changed_at'] is not None else ''}\n'
        embed.add_field(
            name='Username history',
            value=name_history_str,
            inline=False
        )
        await interaction.response.send_message(files=[file, skin_file], embed=embed)

    @minecraft_info.error
    async def say_error(self, interaction: discord.Interaction, error):

        await interaction.response.send_message(embed=embeds.make_error_embed(error), ephemeral=True)

async def setup(bot):
    await bot.add_cog(minecraftCommands(bot))

