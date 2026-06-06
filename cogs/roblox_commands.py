'''
FUTURE COMMANDS:

- get-promotion-channels(username, user_id):
    - not sure
    - show the affiliated channels of the player
'''
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

from templates import embeds
from utils import roblox_tools

class robloxComands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='roblox-info', description='Information about a roblox player')
    async def roblox_info(self, interaction: discord.Interaction, username: str = None, user_id: int = None):
        if username is None and user_id is None: return

        player_profile = roblox_tools.get_player_profile(username, user_id)

        user_id = player_profile['id']
        username = player_profile['name']
        display_name = player_profile['displayName']
        has_verified_badge = player_profile['hasVerifiedBadge']
        is_banned = player_profile['isBanned']
        description = player_profile['description']
        if description == '': description = None
        created = player_profile['created']
        created_date = datetime.fromisoformat(created)

        embed, file = embeds.get_roblox_embed()
        embed.title = f'Roblox information'
        embed.add_field(
            name=f'{username} profile {'🚫' if is_banned else ''}{'<:verified_badge:1512510616093331517>' if has_verified_badge else ''}',
            value=f'> Username: `{username}`\n> Display Name: `{display_name}`\n> User ID: `{user_id}`\n> Account created: `{created_date}`\n> Description: ```{description}```',
            inline=True
        )
        embed.add_field(
            name='Username history',
            value='not functional for now.',
            inline=False
        )
        await interaction.response.send_message(files=[file], embed=embed)

    @roblox_info.error
    async def say_error(self, interaction: discord.Interaction, error):

        await interaction.response.send_message(embed=embeds.make_error_embed(error), ephemeral=True)

    @app_commands.command(name='roblox-badges', description='Show all the badges own by a roblox player')
    async def roblox_badges(self, interaction: discord.Interaction, username: str = None, user_id: int = None):
        if username is None and user_id is None: return
        if not username: username = roblox_tools.get_player_profile(username, user_id)["data"][0]['name']
        badge_list = roblox_tools.get_player_badges(username, user_id)

        def make_embed(index: int):

            embed, file = embeds.get_roblox_embed()
            embed.title = f"{username}'s badges"
            embed.description = f'`{index+1}`/`{len(badge_list)}` Badges'
            embed.add_field(
                name=badge_list[index]['name'],
                value=badge_list[index]['description']
            )
            embed.set_image(
                url=badge_list[index]['imageUrl']
            )
            return embed, file
        
        class NavigationButtons(discord.ui.View):
            def __init__(self, index: int = 0):
                super().__init__()
                self.index = index
                self._update_buttons()
            def _update_buttons(self):
                self.full_back_button.disabled = self.index <= 0
                self.back_button.disabled = self.index <= 0
                self.next_button.disabled = self.index >= len(badge_list) - 1
                self.full_next_button.disabled = self.index >= len(badge_list) - 1
            @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏮️", disabled=True)
            async def full_back_button(self, interaction: discord.Interaction, button: discord.Button):
                self.index = 0
                self._update_buttons()
                embed, file = make_embed(self.index)
                await interaction.response.edit_message(embed=embed, attachments=[file], view=self)
            @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏪", disabled=True)
            async def back_button(self, interaction: discord.Interaction, button: discord.Button):
                if self.index > 0:
                    self.index -= 1
                self._update_buttons()
                embed, file = make_embed(self.index)
                await interaction.response.edit_message(embed=embed, attachments=[file], view=self)
            @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏩")
            async def next_button(self, interaction: discord.Interaction, button: discord.Button):
                if self.index < len(badge_list) - 1:
                    self.index += 1
                self._update_buttons()
                embed, file = make_embed(self.index)
                await interaction.response.edit_message(embed=embed, attachments=[file], view=self)
            @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏭️")
            async def full_next_button(self, interaction: discord.Interaction, button: discord.Button):
                self.index = len(badge_list) - 1
                self._update_buttons()
                embed, file = make_embed(self.index)
                await interaction.response.edit_message(embed=embed, attachments=[file], view=self)

        embed, file = make_embed(0)

        await interaction.response.send_message(embed=embed, files=[file], view=NavigationButtons())

    @roblox_badges.error
    async def say_error(self, interaction: discord.Interaction, error):

        await interaction.response.send_message(embed=embeds.make_error_embed(error), ephemeral=True)


async def setup(bot):
    await bot.add_cog(robloxComands(bot))

