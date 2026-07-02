'''
FUTURE COMMANDS:

- osu-icon-wiki():
    - show all icons with associated value
- osu-achievements
'''

import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

from templates import embeds, exceptions
from utils import osu_tools

class osuComands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='osu-info', description='Information about an Osu! player')
    @app_commands.describe(username='The user name')
    @app_commands.describe(user_id='The user id')
    @app_commands.describe(gamemode='The gamemode you want the info (osu, catch, taiko, mania)')
    async def osu_info(self, interaction: discord.Interaction, username: str = None, user_id: int = None, gamemode: str = 'osu'):
        if username is None and user_id is None: raise exceptions.InvalidInputException('You must provide an **username** or an **user_id**')

        player_profile = osu_tools.get_player_profile(username, user_id, gamemode)
        if not player_profile: raise exceptions.UserNotFoundException(username, user_id)

        # Change osu to standard and fruits to catch for good display
        # Change gamemode emoji for given gamemode
        gamemode_emoji = '<:mania:1512849916706295818>'
        if gamemode == 'osu':
            gamemode = 'standard'
            gamemode_emoji = '<:standard:1512849884313686107>'
        elif gamemode == 'catch': gamemode_emoji = '<:fruits:1512849871990952047>'
        elif gamemode == 'taiko': gamemode_emoji = '<:taiko:1512849895873052885>'

        follower_count  = player_profile['follower_count']
        playmode            = player_profile['playmode']
        user_id             = player_profile['id']
        username            = player_profile['username']
        previous_usernames  = player_profile['previous_usernames']
        previous_usernames  = [username] + previous_usernames[0:] # add current username on top fo the current usernames
        profile_colour      = player_profile['profile_colour']
        avatar_url          = player_profile['avatar_url']
        cover_url           = player_profile['cover_url']
        is_bot              = player_profile['is_bot']
        is_online           = player_profile['is_online']
        is_deleted          = player_profile['is_deleted']
        is_supporter        = player_profile['is_supporter']
        country             = player_profile['country']['name']
        country_code        = player_profile['country']['code']
        interests           = player_profile['interests']
        occupation          = player_profile['occupation']
        play_count          = player_profile['statistics']['play_count']
        global_rank         = player_profile['statistics']['global_rank']
        country_rank        = player_profile['statistics']['country_rank']
        pp                  = player_profile['statistics']['pp']
        play_time           = player_profile['statistics']['play_time']
        ss                  = player_profile['statistics']['grade_counts']['ss']
        s                   = player_profile['statistics']['grade_counts']['s']
        a                   = player_profile['statistics']['grade_counts']['a']
        level               = player_profile['statistics']['level']['current']
        level_progress      = player_profile['statistics']['level']['progress']
        best_global_rank    = player_profile['rank_highest']['rank']
        best_updtat         = player_profile['rank_highest']['updated_at']
        best_updtat_date    = datetime.fromisoformat(best_updtat)

        embed, file = embeds.get_osu_embed()
        embed.title = f'{gamemode_emoji} Osu!{gamemode} information'
        embed.url   = f'https://osu.ppy.sh/users/{user_id}'
        embed.add_field(
            name=f'{username} profile'
            f'{' :wastebasket:' if is_deleted else ''}'
            f'{' :robot:' if is_bot else ''}'
            f'{' <:osu_supporter:1512764689476747458>' if is_supporter else ''}'
            f'{' :green_circle:' if is_online else ' :red_circle:'}',
            value=
            f'> **Username:** `{username}`'
            f'\n> **User ID:** `{user_id}`'
            f'\n> **Country:** :flag_{country_code.lower()}: `{country}`'
            f'{f'\n> **Interests:** `{interests}`' if interests is not None else ''}'
            f'{f'\n> **Occupation:** `{occupation}`' if occupation is not None else ''}'
            f'\n> **Main:** `{playmode}`'
            f'\n> **Followers:** `{follower_count}`',
            inline=True
        )
        embed.add_field(
            name=f'osu!{gamemode}',
            value=
            f'\n> **Play Count:** `{play_count}`'
            f'\n> **PP:** `{pp}`'
            f'\n> **Play time:** `{play_time}`'
            f'\n> **Level:** `{level} ({level_progress})`',
            inline=True
        )
        embed.add_field(
            name='Rank',
            value=
            f'> **Global rank:** `{global_rank}`'
            f'\n> **Best global rank:** `{best_global_rank}` *{best_updtat_date}*'
            f'\n> **Country rank:** `{country_rank}`',
            inline=False
        )
        embed.add_field(
            name='Grade counts',
            value=
            f'> <:ss_grade:1512849863941951528> **:** `{ss}`'
            f'\n> <:s_grade:1512849856757104852> **:** `{s}`'
            f'\n> <:a_grade:1512849823613714463> **:** `{a}`',
            inline=True
        )
        username_history_str = ''
        for i in range(len(previous_usernames)):
            username_history_str += f'> **{i+1}.** `{previous_usernames[i]}` {'(current)' if i == 0 else ''}\n'
        embed.add_field(
            name='Username history',
            value=username_history_str,
            inline=True
        )
        embed.set_thumbnail(
            url=avatar_url,
        )
        embed.set_image(
            url=cover_url
        )
        await interaction.response.send_message(files=[file], embed=embed)

    @osu_info.error
    async def say_error(self, interaction: discord.Interaction, error):

        await interaction.response.send_message(embed=embeds.make_error_embed(error), ephemeral=True)

async def setup(bot):
    await bot.add_cog(osuComands(bot))
