import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import base64

from templates import embeds, emojis
from utils import gd_formatter, gd_tools

class gdComands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='gd-info', description='Information about a Geometry Dash player')
    async def gd_info(self, interaction: discord.Interaction, username: str = None, user_id: int = None, account_id: int = None):
        if username is None and account_id is None: return

        # DOC: https://wyliemaster.github.io/gddocs/#/resources/server/user
        player_profile  = gd_formatter.to_dict(gd_tools.get_player_profile(username=username, user_id=user_id, account_id=account_id))[0]

        username        = player_profile.get('1', None)
        user_id         = player_profile.get('2', None)
        account_id      = player_profile.get('16', None)

        mod_level       = int(player_profile.get('49', None))
        mod_level_emoji = None
        if mod_level == 1:
            mod_level_emoji = emojis.emoji_dict.get('normal_mod')
        elif mod_level == 2:
            mod_level_emoji = emojis.emoji_dict.get('elder_mod')
        elif mod_level == 3: # Not documented but i think it has a 4th code for lb mods (there is no 4th one but maybe one day)
            mod_level_emoji = emojis.emoji_dict.get('leaderboard_mod')

        demons          = player_profile.get('4', None)
        creator_points  = player_profile.get('8', None)
        global_rank     = int(player_profile.get('30', None))
        global_rank_emoji = emojis.emoji_dict.get('lb_trophy_11')
        if global_rank == 0:
            global_rank_emoji = None
        elif 50000 >= global_rank > 10000: # rank is within 50k an 10.001
            global_rank_emoji = emojis.emoji_dict.get('lb_trophy_10')
        elif 10000 >= global_rank > 5000: # rank is within 10k an 5.001
            global_rank_emoji = emojis.emoji_dict.get('lb_trophy_09')
        elif 5000 >= global_rank > 1000: # rank is within 5k an 1.001
            global_rank_emoji = emojis.emoji_dict.get('lb_trophy_08')
        elif 1000 >= global_rank > 500: # rank is within 1k an 501
            global_rank_emoji = emojis.emoji_dict.get('lb_trophy_07')
        elif 500 >= global_rank > 200: # rank is within 500 an 201
            global_rank_emoji = emojis.emoji_dict.get('lb_trophy_06')
        elif 200 >= global_rank > 100: # rank is within 200 an 101
            global_rank_emoji = emojis.emoji_dict.get('lb_trophy_05')
        elif 100 >= global_rank > 50: # rank is within 100 an 51
            global_rank_emoji = emojis.emoji_dict.get('lb_trophy_04')
        elif 50 >= global_rank > 10: # rank is within 50 an 11
            global_rank_emoji = emojis.emoji_dict.get('lb_trophy_03')
        elif 10 >= global_rank > 1: # rank is within 10 an 2
            global_rank_emoji = emojis.emoji_dict.get('lb_trophy_02')
        elif global_rank == 1: # rank is 1
            global_rank_emoji = emojis.emoji_dict.get('lb_trophy_01')

        stars           = player_profile.get('3', 0)
        secret_coins    = player_profile.get('13', 0)
        user_coins      = player_profile.get('17', 0)
        diamonds        = player_profile.get('46', 0)
        moons           = player_profile.get('52', 0)

        youtube         = player_profile.get('20', None)
        twitter         = player_profile.get('44', None)
        twitch          = player_profile.get('45', None)
        discord         = player_profile.get('58', None)
        instagram       = player_profile.get('59', None)
        tiktok          = player_profile.get('60', None)

        base_levels     = player_profile.get('56', None)
        auto            = base_levels[0] if base_levels else 0
        easy            = base_levels[1] if base_levels else 0
        normal          = base_levels[2] if base_levels else 0
        hard            = base_levels[3] if base_levels else 0
        harder          = base_levels[4] if base_levels else 0
        insane          = base_levels[5] if base_levels else 0

        plat_levels     = player_profile.get('57', None)
        auto_plat       = plat_levels[0] if plat_levels else 0
        easy_plat       = plat_levels[1] if plat_levels else 0
        normal_plat     = plat_levels[2] if plat_levels else 0
        hard_plat       = plat_levels[3] if plat_levels else 0
        harder_plat     = plat_levels[4] if plat_levels else 0
        insane_plat     = plat_levels[5] if plat_levels else 0

        demons_levels       = player_profile.get('55', None)
        easy_demon          = demons_levels[0] if demons_levels else 0
        medium_demon        = demons_levels[1] if demons_levels else 0
        hard_demon          = demons_levels[2] if demons_levels else 0
        insane_demon        = demons_levels[3] if demons_levels else 0
        extreme_demon       = demons_levels[4] if demons_levels else 0
        easy_demon_plat     = demons_levels[5] if demons_levels else 0
        medium_demon_plat   = demons_levels[6] if demons_levels else 0
        hard_demon_plat     = demons_levels[7] if demons_levels else 0
        insane_demon_plat   = demons_levels[8] if demons_levels else 0
        extreme_demon_plat  = demons_levels[9] if demons_levels else 0

        embed, file = embeds.get_gd_embed()
        embed.title = f'Geometry Dash information'
        embed.url   = f'https://gdbrowser.com/u/{username}'
        embed.add_field(
            name=f"{username} profile"
            f"{f' {mod_level_emoji}' if mod_level_emoji else ''}",
            value=(
                f"> **Username:** `{username}`"
                f"\n> **User ID:** `{user_id}`"
                f"\n> **Account ID:** `{account_id}`"
                f"\n> {f'{global_rank_emoji} **:** `{global_rank}`' if global_rank_emoji else '**Not ranked**'}"
                f"\n> {emojis.emoji_dict.get('demon')} **:** `{demons}`"
                f"{f'\n> {emojis.emoji_dict.get('discord')} **:** `{discord}`' if discord else ''}"
            ),
            inline=True
        )
        embed.add_field(
            name="Resources",
            value=(
                f"> {emojis.emoji_dict.get('star')} **:** `{stars}`"
                f"\n> {emojis.emoji_dict.get('moon')} **:** `{moons}`"
                f"\n> {emojis.emoji_dict.get('diamond')} **:** `{diamonds}`"
                f"\n> {emojis.emoji_dict.get('user_coins')} **:** `{user_coins}`"
                f"\n> {emojis.emoji_dict.get('secret_coin')} **:** `{secret_coins}`"
                f"\n> {emojis.emoji_dict.get('creator_points')} **:** `{creator_points}`"
            ),
            inline=True
        )
        if base_levels or plat_levels:
            embed.add_field(
                name="Levels | Platformers",
                value=(
                    f"> {emojis.emoji_dict.get('auto')} **:** `{auto} | {auto_plat}`"
                    f"\n> {emojis.emoji_dict.get('easy')} **:** `{easy} | {easy_plat}`"
                    f"\n> {emojis.emoji_dict.get('normal')} **:** `{normal} | {normal_plat}`"
                    f"\n> {emojis.emoji_dict.get('hard')} **:** `{hard} | {hard_plat}`"
                    f"\n> {emojis.emoji_dict.get('harder')} **:** `{harder} | {harder_plat}`"
                    f"\n> {emojis.emoji_dict.get('insane')} **:** `{insane} | {insane_plat}`"
                    f"\n> {emojis.emoji_dict.get('easy_demon')} **:** `{easy_demon} | {easy_demon_plat}`"
                    f"\n> {emojis.emoji_dict.get('medium_demon')} **:** `{medium_demon} | {medium_demon_plat}`"
                    f"\n> {emojis.emoji_dict.get('demon')} **:** `{hard_demon} | {hard_demon_plat}`"
                    f"\n> {emojis.emoji_dict.get('insane_demon')} **:** `{insane_demon} | {insane_demon_plat}`"
                    f"\n> {emojis.emoji_dict.get('extreme_demon')} **:** `{extreme_demon} | {extreme_demon_plat}`"
                ),
                inline=True
            )
        if youtube or twitter or twitch or instagram or tiktok:
            embed.add_field(
                name="",
                value=(
                    f"[{emojis.emoji_dict.get('youtube')}](https://www.youtube.com/channel/{youtube}) " if youtube else ""
                    f"[{emojis.emoji_dict.get('twitter')}](https://x.com/{twitter}) " if twitter else ""
                    f"[{emojis.emoji_dict.get('twitch')}](https://www.twitch.tv/{twitch}) " if twitch else ""
                    f"[{emojis.emoji_dict.get('instagram')}](https://www.instagram.com/{instagram}) " if instagram else ""
                    f"[{emojis.emoji_dict.get('tiktok')}](https://www.tiktok.com/@{tiktok}) " if tiktok else ""
                ),
                inline=False
            )
        await interaction.response.send_message(files=[file], embed=embed)

    @gd_info.error
    async def say_error(self, interaction: discord.Interaction, error):

        await interaction.response.send_message(embed=embeds.make_error_embed(error), ephemeral=True)

    @app_commands.command(name='gd-icons', description='Show icons of a Geometry Dash player')
    async def gd_icons(self, interaction: discord.Interaction, username: str = None, user_id: int = None, account_id: int = None):
        if username is None and user_id is None: return

        # DOC: https://wyliemaster.github.io/gddocs/#/resources/server/user
        player_profile  = gd_formatter.to_dict(gd_tools.get_player_profile(username, user_id, account_id))[0]

        username        = player_profile.get('1', None)
        user_id         = player_profile.get('2', None)

        acc_icon        = player_profile.get('21', None)
        acc_ship        = player_profile.get('22', None)
        acc_ball        = player_profile.get('23', None)
        acc_bird        = player_profile.get('24', None)
        acc_dart        = player_profile.get('25', None)
        acc_robot       = player_profile.get('26', None)
        acc_glow        = player_profile.get('28', None)
        acc_spider      = player_profile.get('43', None)
        acc_explosion   = player_profile.get('48', None)
        acc_swing       = player_profile.get('53', None)
        acc_jetpack     = player_profile.get('54', None)

        icon_list = [
            f'https://gdbrowser.com/iconkit/premade/cube_{acc_icon}.png',
            f'https://gdbrowser.com/iconkit/premade/ship_{acc_ship}.png',
            f'https://gdbrowser.com/iconkit/premade/ball_{acc_ball}.png',
            f'https://gdbrowser.com/iconkit/premade/ufo_{acc_bird}.png',
            f'https://gdbrowser.com/iconkit/premade/wave_{acc_dart}.png',
            f'https://gdbrowser.com/iconkit/premade/robot_{acc_robot}.png',
            f'https://gdbrowser.com/iconkit/premade/spider_{acc_spider}.png',
            f'https://gdbrowser.com/iconkit/premade/swing_{acc_swing}.png',
            f'https://gdbrowser.com/iconkit/premade/jetpack_{acc_jetpack}.png',
        ]
        icon_type = [
            'Cube',
            'Ship',
            'Ball',
            'Ufo',
            'Wave',
            'Robot',
            'Spider',
            'Swing',
            'Jetpack',
        ]

        def make_embed(index: int):

            embed, file = embeds.get_gd_embed()
            embed.title = f"{username}'s icons"
            embed.add_field(
                name=f'{icon_type[index]}',
                value='',
                inline=True
            )
            embed.set_image(
                url=icon_list[index]
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
                self.next_button.disabled = self.index >= len(icon_list) - 1
                self.full_next_button.disabled = self.index >= len(icon_list) - 1
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
                if self.index < len(icon_list) - 1:
                    self.index += 1
                self._update_buttons()
                embed, file = make_embed(self.index)
                await interaction.response.edit_message(embed=embed, attachments=[file], view=self)
            @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏭️")
            async def full_next_button(self, interaction: discord.Interaction, button: discord.Button):
                self.index = len(icon_list) - 1
                self._update_buttons()
                embed, file = make_embed(self.index)
                await interaction.response.edit_message(embed=embed, attachments=[file], view=self)

        embed, file = make_embed(0)
        await interaction.response.send_message(files=[file], embed=embed, view=NavigationButtons())

    @gd_icons.error
    async def say_error(self, interaction: discord.Interaction, error):

        await interaction.response.send_message(embed=embeds.make_error_embed(error), ephemeral=True)

    @app_commands.command(name='gd-level-info', description='Information about a Geometry Dash level')
    async def gd_level_info(self, interaction: discord.Interaction, level_id: int):
        
        # DOC: https://wyliemaster.github.io/gddocs/#/resources/server/level
        # DOC: https://wyliemaster.github.io/gddocs/#/resources/server/user
        # DOC: https://wyliemaster.github.io/gddocs/#/resources/server/song
        level_profile   = gd_formatter.to_dict(gd_tools.get_level_data(level_id))[0]

        level_id        = level_profile.get('1', None)
        original_level_id = level_profile.get('30', None)
        is_copied       = False
        if original_level_id != level_id:
            is_copied = True

        level_name      = level_profile.get('2', None)
        description     = level_profile.get('3', None) # Base 64 encoded

        is_demon        = int(level_profile.get('17', None))
        is_auto         = level_profile.get('25', None)

        epic_diff       = int(level_profile.get('42', None))

        diff_emoji = None
        diff_denominator= level_profile.get('8', None)
        diff_nominator  = int(level_profile.get('9', None))
        demon_difficulty= int(level_profile.get('43', None))
        if is_auto: # auto
            diff_emoji = emojis.emoji_dict.get('auto')
        elif is_demon == 1:
            match(demon_difficulty, epic_diff):
                case(3, 0): # Easy
                    diff_emoji = emojis.emoji_dict.get('easy_demon')
                case(3, 1):
                    diff_emoji = emojis.emoji_dict.get('easy_demon_epic')
                case(3, 2):
                    diff_emoji = emojis.emoji_dict.get('easy_demon_legendary')
                case(3, 3):
                    diff_emoji = emojis.emoji_dict.get('easy_demon_mythic')
                case(4, 0): # Medium
                    diff_emoji = emojis.emoji_dict.get('medium_demon')
                case(4, 1):
                    diff_emoji = emojis.emoji_dict.get('medium_demon_epic')
                case(4, 2):
                    diff_emoji = emojis.emoji_dict.get('medium_demon_legendary')
                case(4, 3):
                    diff_emoji = emojis.emoji_dict.get('medium_demon')
                case(0, 0): # Hard
                    diff_emoji = emojis.emoji_dict.get('demon')
                case(0, 1):
                    diff_emoji = emojis.emoji_dict.get('demon_epic')
                case(0, 2):
                    diff_emoji = emojis.emoji_dict.get('demon_legendary')
                case(0, 3):
                    diff_emoji = emojis.emoji_dict.get('demon')
                case(5, 0): # Insane
                    diff_emoji = emojis.emoji_dict.get('insane_demon')
                case(5, 1):
                    diff_emoji = emojis.emoji_dict.get('insane_demon_epic')
                case(5, 2):
                    diff_emoji = emojis.emoji_dict.get('insane_demon_legendary')
                case(5, 3):
                    diff_emoji = emojis.emoji_dict.get('insane_demon')
                case(6, 0): # Extreme
                    diff_emoji = emojis.emoji_dict.get('extreme_demon')
                case(6, 1):
                    diff_emoji = emojis.emoji_dict.get('extreme_demon_epic')
                case(6, 2):
                    diff_emoji = emojis.emoji_dict.get('extreme_demon_legendary')
                case(6, 3):
                    diff_emoji = emojis.emoji_dict.get('extreme_demon_mythic')
        else:
            if diff_nominator == 0: # N/A
                diff_emoji = emojis.emoji_dict.get('unrated')
            match(diff_nominator, epic_diff):
                case (10, 0): # Easy
                    diff_emoji = emojis.emoji_dict.get('easy')
                case (10, 1):
                    diff_emoji = emojis.emoji_dict.get('easy_epic')
                case (10, 2):
                    diff_emoji = emojis.emoji_dict.get('easy_legendary')
                case (10, 3):
                    diff_emoji = emojis.emoji_dict.get('easy_mythic')
                case (20, 0): # Normal
                    diff_emoji = emojis.emoji_dict.get('normal')
                case (20, 1):
                    diff_emoji = emojis.emoji_dict.get('normal_epic')
                case (20, 2):
                    diff_emoji = emojis.emoji_dict.get('normal_legendary')
                case (20, 3):
                    diff_emoji = emojis.emoji_dict.get('normal_mythic')
                case (30, 0): # Hard
                    diff_emoji = emojis.emoji_dict.get('hard')
                case (30, 1):
                    diff_emoji = emojis.emoji_dict.get('hard_epic')
                case (30, 2):
                    diff_emoji = emojis.emoji_dict.get('hard_legendary')
                case (30, 3):
                    diff_emoji = emojis.emoji_dict.get('hard_mythic')
                case (40, 0): # Harder
                    diff_emoji = emojis.emoji_dict.get('harder')
                case (40, 1):
                    diff_emoji = emojis.emoji_dict.get('harder_epic')
                case (40, 2):
                    diff_emoji = emojis.emoji_dict.get('harder_legendary')
                case (40, 3):
                    diff_emoji = emojis.emoji_dict.get('harder_mythic')
                case (50, 0): # Insane
                    diff_emoji = emojis.emoji_dict.get('insane')
                case (50, 1):
                    diff_emoji = emojis.emoji_dict.get('insane_epic')
                case (50, 2):
                    diff_emoji = emojis.emoji_dict.get('insane_legendary')
                case (50, 3):
                    diff_emoji = emojis.emoji_dict.get('insane_mythic')

        lenght          = int(level_profile.get('15', None))
        lenght_name     = None
        if lenght == 0: # Tiny
            lenght_name = 'Tiny'
        if lenght == 1: # Small
            lenght_name = 'Small'
        elif lenght == 2: # Medium
            lenght_name = 'Medium'
        elif lenght == 3: # Long
            lenght_name = 'Long'
        elif lenght == 4: # XL
            lenght_name = 'XL'
        elif lenght == 5: # Platformer
            lenght_name = 'Platformer'
            
        downloads       = level_profile.get('10', None)
        likes           = level_profile.get('14', None)
        stars           = level_profile.get('18', None)
        
        creator_id      = level_profile.get('6', None)
        creator_profile = gd_formatter.to_dict(gd_tools.get_player_profile(user_id=creator_id))[0]
        creator_name    = creator_profile.get('1', None)

        song_id         = level_profile.get('35', None)
        song_profile    = gd_formatter.to_dict_song(gd_tools.get_song_data(song_id=song_id))
        song_name       = song_profile[0].get('2', None)
        song_creator    = song_profile[0].get('4', None)

        coins_number    = int(level_profile.get('37', None))
        coins_verified  = int(level_profile.get('38', None)) # 0 or 1
        coins_emoji     = '<:user_coins:1520060202559209583>' if coins_verified==1 else '<:user_coins_unverified:1520750888363233311>'
        
        embed, file = embeds.get_gd_embed()
        embed.title = f'Geometry Dash level information'
        embed.url   = f'https://gdbrowser.com/{level_id}'
        embed.add_field(
            name=(
                "Level"
                f" {diff_emoji if diff_emoji else ''}"
                f" {emojis.emoji_dict.get('copied') if is_copied else ''}"
                f" {coins_emoji * coins_number}"
            ),
            value=(
                f"> **Level name:** `{level_name}`"
                f"\n> **Level ID:** `{level_id}`"
                f"{f'\n> **Original level ID:** `{original_level_id}`' if is_copied else ''}"
                f"\n> **Creator:** `{creator_name}`"
                f"\n> {emojis.emoji_dict.get('download')} **:** `{downloads}`"
                f"\n> {emojis.emoji_dict.get('like')} **:** `{likes}`"
                f"\n> {emojis.emoji_dict.get('star')} **:** `{stars}`"
                f"\n> {emojis.emoji_dict.get('time')} **:** `{lenght_name}`"
                f"\n> **Description:** ```{base64.b64decode(description).decode('utf-8') if description else 'None'}```"
            ),
            inline=True
        )
        embed.add_field(
            name="Song",
            value=(
                f"[{emojis.emoji_dict.get('playsong')}]({f'https://www.newgrounds.com/audio/listen/{song_id}'})"
                f"\n> **Name:** `{song_name}`"
                f"\n> **Song ID:** `{song_id}`"
                f"\n> **Creator:** `{song_creator}`"
            ),
            inline=True
        )
        await interaction.response.send_message(files=[file], embed=embed)

    @gd_level_info.error
    async def say_error(self, interaction: discord.Interaction, error):
        
        await interaction.response.send_message(embed=embeds.make_error_embed(error), ephemeral=True)

async def setup(bot):
    await bot.add_cog(gdComands(bot))

