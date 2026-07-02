import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

from templates import embeds, exceptions, emojis
from utils import roblox_tools

class robloxComands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='roblox-info', description='Information about a roblox player')
    @app_commands.describe(username='The user name')
    @app_commands.describe(user_id='The user id')
    async def roblox_info(self, interaction: discord.Interaction, username: str = None, user_id: int = None):
        if username is None and user_id is None:
            raise exceptions.InvalidInputException('You must provide an **user_id** or an **username**')

        player_profile      = roblox_tools.get_player_profile(username, user_id)
        if not player_profile:
            raise exceptions.UserNotFoundException(username, user_id)
        user_id             = player_profile.get('id', None)
        username            = player_profile.get('name', None)
        display_name        = player_profile.get('displayName', None)
        has_verified_badge  = player_profile.get('hasVerifiedBadge', None)
        is_banned           = player_profile.get('isBanned', None)
        description         = player_profile.get('description', None)
        if description == '':
            description = None
        created             = player_profile.get('created', None)
        created_date        = datetime.fromisoformat(created)

        player_thumbnail    = roblox_tools.get_player_headshot(user_id)["data"][0]
        thumbnail_url       = player_thumbnail['imageUrl']

        # 0: Offline | 1: Online | 2: In Game | 3: In Studio | 4: Invisible
        player_presence     = roblox_tools.get_user_presence(user_id)
        user_presence_type  = player_presence['userPresences'][0]['userPresenceType']
        user_presence_emoji = ""
        if user_presence_type==0:
            user_presence_emoji = ' :red_circle:'
        elif user_presence_type==1:
            user_presence_emoji = ' :blue_circle:'
        elif user_presence_type==2:
            user_presence_emoji = ' :green_circle:'
        elif user_presence_type==3:
            user_presence_emoji = ' <:roblox_studio:1513253052084125736>'
        elif user_presence_type==4:
            user_presence_emoji = ' :white_circle:'

        premium = roblox_tools.get_user_premium_membership(user_id)

        followers = roblox_tools.get_user_followers(user_id).get('count', 0)
        followings = roblox_tools.get_user_followings(user_id).get('count', 0)

        embed, file = embeds.get_roblox_embed()
        embed.title = f'Roblox information'
        embed.url   = f'https://roblox.com/users/{user_id}/profile'
        embed.add_field(
            name=f'{username} profile'
            f'{' :no_entry_sign:' if is_banned else ''}'
            f'{' <:verified_badge:1512510616093331517>' if has_verified_badge else ''}'
            f'{' <:roblox_premium:1513519712351551638>' if premium else ''}'
            f'{user_presence_emoji}',
            value=f'> **Username:** `{username}`'
            f'\n> **Display Name:** `{display_name}`'
            f'\n> **User ID:** `{user_id}`'
            f'\n> **Followers:** `{followers}`'
            f'\n> **Followings:** `{followings}`'
            f'\n> **Account created:** `{created_date}`'
            f'\n> **Description:** ``` {description} ```', # keep spaces between discord format cause of link breaking the format
            inline=True
        )
        embed.add_field(
            name='Username history',
            value='not functional for now.',
            inline=False
        )
        embed.set_thumbnail(
            url=thumbnail_url
        )
        await interaction.response.send_message(files=[file], embed=embed)

    @app_commands.command(name='roblox-badges', description='Show all the badges own by a roblox player')
    @app_commands.describe(username='The user name')
    @app_commands.describe(user_id='The user id')
    async def roblox_badges(self, interaction: discord.Interaction, username: str = None, user_id: int = None):
        if username is None and user_id is None: raise exceptions.InvalidInputException('You must provide an **user_id** or an **username**')
        if not username:
            player_profile = roblox_tools.get_player_profile(username, user_id)
            if not player_profile: raise exceptions.UserNotFoundException(username, user_id)
            username = player_profile.get('name', None)
        if not user_id:
            player_profile = roblox_tools.get_player_profile(username, user_id)
            if not player_profile: raise exceptions.UserNotFoundException(username, user_id)
            user_id = player_profile.get('id', None)

        badge_list = roblox_tools.get_player_badges(user_id)

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

    @app_commands.command(name='roblox-outfit', description='Show the outfit of a roblox player')
    @app_commands.describe(username='The user name')
    @app_commands.describe(user_id='The user id')
    async def roblox_outfit(self, interaction: discord.Interaction, username: str = None, user_id: int = None):
        if username is None and user_id is None: raise exceptions.InvalidInputException('You must provide an **user_id** or an **username**')
        if not username:
            player_profile = roblox_tools.get_player_profile(username, user_id)
            if not player_profile: raise exceptions.UserNotFoundException(username, user_id)
            username = player_profile.get('name', None)
        if not user_id:
            player_profile = roblox_tools.get_player_profile(username, user_id)
            if not player_profile: raise exceptions.UserNotFoundException(username, user_id)
            user_id = player_profile.get('id', None)

        player_outfit = roblox_tools.get_player_full_body(user_id)["data"][0]
        player_outfit_url = player_outfit['imageUrl']
        def make_embed(tab: str = 'info', index: int = None):

            embed, file = embeds.get_roblox_embed()
            embed.title = f"{username}'s outfit"
            embed.description = f'' # maybe robux cost ?
            embed.set_thumbnail(
                url=player_outfit_url
            )

            player_outfit_details = roblox_tools.get_ouftfit_details(user_id)

            # tabs: info, assets, emotes
            if tab == 'info':
                height = player_outfit_details['scales']['height']
                width = player_outfit_details['scales']['width']
                head = player_outfit_details['scales']['head']
                depth = player_outfit_details['scales']['depth']
                embed.add_field(
                    name='Scales',
                    value=
                    f'> Height: `{height}`'
                    f'\n> Width: `{width}`'
                    f'\n> Head: `{head}`'
                    f'\n> Depth: `{depth}`',
                    inline=True
                )

                return embed, file

            elif tab == 'assets':
                assets = player_outfit_details['assets']
                asset = assets[index]
                name = asset['name']
                asset_id = asset['id']
                asset_type = asset['assetType']['name']

                asset_thumbnail = roblox_tools.get_asset_thumbnail(asset_id)["data"][0]
                asset_thumbnail_url = asset_thumbnail['imageUrl']

                embed.description = f'`{index+1}`/`{len(assets)}` Assets' # maybe robux cost ?
                embed.add_field(
                    name='',
                    value=
                    f'> Name: `{name}`'
                    f'\n> Asset ID: `{asset_id}`'
                    f'\n> Type: `{asset_type}`',
                    inline=True
                )
                embed.add_field(
                    name='',
                    value=f'https://www.roblox.com/catalog/{asset_id}',
                    inline=False
                )
                embed.set_image(
                    url=asset_thumbnail_url
                )
                class NavigationButtons(discord.ui.View):
                    def __init__(self, index: int = 0):
                        super().__init__()
                        self.index = index
                        self._update_buttons()
                    def _update_buttons(self):
                        self.full_back_button.disabled = self.index <= 0
                        self.back_button.disabled = self.index <= 0
                        self.next_button.disabled = self.index >= len(assets) - 1
                        self.full_next_button.disabled = self.index >= len(assets) - 1
                    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏮️", disabled=True)
                    async def full_back_button(self, interaction: discord.Interaction, button: discord.Button):
                        self.index = 0
                        self._update_buttons()
                        embed, file, view = make_embed('assets', self.index)
                        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)
                    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏪", disabled=True)
                    async def back_button(self, interaction: discord.Interaction, button: discord.Button):
                        if self.index > 0:
                            self.index -= 1
                        self._update_buttons()
                        embed, file, view = make_embed('assets', self.index)
                        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)
                    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏩")
                    async def next_button(self, interaction: discord.Interaction, button: discord.Button):
                        if self.index < len(assets) - 1:
                            self.index += 1
                        self._update_buttons()
                        embed, file, view = make_embed('assets', self.index)
                        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)
                    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏭️")
                    async def full_next_button(self, interaction: discord.Interaction, button: discord.Button):
                        self.index = len(assets) - 1
                        self._update_buttons()
                        embed, file, view = make_embed('assets', self.index)
                        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)
                    @discord.ui.button(label='Back', style=discord.ButtonStyle.red, emoji="↩️")
                    async def return_button(self, interaction: discord.Interaction, button: discord.Button):
                        embed, file = make_embed()
                        view = SelectionButtons()
                        await interaction.response.edit_message(embed=embed, attachments=[file], view=view)
                view = NavigationButtons()

            elif tab == 'emotes':
                emotes = player_outfit_details['emotes']
                emote = emotes[index]
                name = emote['assetName']
                asset_id = emote['assetId']

                emote_thumbnail = roblox_tools.get_asset_thumbnail(asset_id)["data"][0]
                emote_thumbnail_url = emote_thumbnail['imageUrl']

                embed.description = f'`{index+1}`/`{len(emotes)}` Emotes' # maybe robux cost ?
                embed.add_field(
                    name='',
                    value=
                    f'> Name: `{name}`'
                    f'\n> Asset ID: `{asset_id}`',
                    inline=True
                )
                embed.add_field(
                    name='',
                    value=f'https://www.roblox.com/catalog/{asset_id}',
                    inline=False
                )
                embed.set_image(
                    url=emote_thumbnail_url
                )
                class NavigationButtons(discord.ui.View):
                    def __init__(self, index: int = 0):
                        super().__init__()
                        self.index = index
                        self._update_buttons()
                    def _update_buttons(self):
                        self.full_back_button.disabled = self.index <= 0
                        self.back_button.disabled = self.index <= 0
                        self.next_button.disabled = self.index >= len(emotes) - 1
                        self.full_next_button.disabled = self.index >= len(emotes) - 1
                    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏮️", disabled=True)
                    async def full_back_button(self, interaction: discord.Interaction, button: discord.Button):
                        self.index = 0
                        self._update_buttons()
                        embed, file, view = make_embed('emotes', self.index)
                        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)
                    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏪", disabled=True)
                    async def back_button(self, interaction: discord.Interaction, button: discord.Button):
                        if self.index > 0:
                            self.index -= 1
                        self._update_buttons()
                        embed, file, view = make_embed('emotes', self.index)
                        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)
                    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏩")
                    async def next_button(self, interaction: discord.Interaction, button: discord.Button):
                        if self.index < len(emotes) - 1:
                            self.index += 1
                        self._update_buttons()
                        embed, file, view = make_embed('emotes', self.index)
                        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)
                    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏭️")
                    async def full_next_button(self, interaction: discord.Interaction, button: discord.Button):
                        self.index = len(emotes) - 1
                        self._update_buttons()
                        embed, file, view = make_embed('emotes', self.index)
                        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)
                    @discord.ui.button(label='Back', style=discord.ButtonStyle.red, emoji="↩️")
                    async def return_button(self, interaction: discord.Interaction, button: discord.Button):
                        embed, file = make_embed()
                        view = SelectionButtons()
                        await interaction.response.edit_message(embed=embed, attachments=[file], view=view)
                view = NavigationButtons()

            return embed, file, view

        class SelectionButtons(discord.ui.View):
            def __init__(self, tab: str = 'info'):
                super().__init__()
                self.tab = tab
                self._update_buttons()
            def _update_buttons(self):
                self.assets_button.disabled = self.tab == 'assets'
                self.emotes_button.disabled = self.tab == 'emotes'
            @discord.ui.button(label='Assets', style=discord.ButtonStyle.red, emoji="👜", disabled=True)
            async def assets_button(self, interaction: discord.Interaction, button: discord.Button):
                self.tab = 'assets'
                self._update_buttons()
                embed, file, view = make_embed(self.tab, 0)
                await interaction.response.edit_message(embed=embed, attachments=[file], view=view)
            @discord.ui.button(label='Emotes', style=discord.ButtonStyle.green, emoji="🕺")
            async def emotes_button(self, interaction: discord.Interaction, button: discord.Button):
                self.tab = 'emotes'
                self._update_buttons()
                embed, file, view = make_embed(self.tab, 0)
                await interaction.response.edit_message(embed=embed, attachments=[file], view=view)
        embed, file = make_embed()

        await interaction.response.send_message(embed=embed, files=[file], view=SelectionButtons())

    @app_commands.command(name='roblox-place-info', description='Information about a roblox place')
    @app_commands.describe(place_id='The place id')
    async def roblox_place_info(self, interaction: discord.Interaction, place_id: int):
        if place_id is None: raise exceptions.InvalidInputException('You must provide a **place_id**')

        place_info      = roblox_tools.get_place_info(place_id).get('data')[0]
        if not place_info: raise exceptions.PlaceNotFoundException(place_id)

        id              = place_info.get('rootPlaceId')
        name            = place_info.get('name')
        description     = place_info.get('description')
        price           = place_info.get('price')
        playing         = place_info.get('playing')
        visits          = place_info.get('visits')
        server_size     = place_info.get('maxPlayers')
        favorites       = place_info.get('favoritedCount')

        created         = place_info.get('created')
        created_date    = datetime.fromisoformat(str(created))
        updated         = place_info.get('updated')
        updated_date    = datetime.fromisoformat(str(updated))

        copying_allowed = place_info.get('copyingAllowed')

        genre = place_info.get('genre_l1')
        subgenre = place_info.get('genre_l2')

        creator     = place_info.get('creator')
        creator_name= creator.get('name')
        creator_id  = creator.get('id')
        creator_type= creator.get('type')
        is_verified    = creator.get('hasVerifiedBadge')

        thumbnail = roblox_tools.get_place_thumbnail(place_id).get('data')[0]
        thumbnail_url = thumbnail.get('imageUrl')

        place_url   = 'https://roblox.com' + place_info.get('canonicalUrlPath')

        n_description = ''
        split_description = description.split('\n')
        n_description += split_description[0]
        for i in range(0, len(split_description)-1):
            n_description += f'\n> {split_description[i+1]}'

        embed, file = embeds.get_roblox_embed()
        embed.title = f'Roblox place information'
        embed.url   = place_url
        embed.add_field(
            name="Place",
            value=(
                f"> **Name:** `{name}`"
                f"\n> **Place id:** `{id}`"
                f"\n> **Active:** `{playing}`"
                f"\n> **Visits:** `{visits}`"
                f"\n> **Favorite:** `{favorites}`"
                f"\n> **Server size:** `{server_size}`"
                f"\n> **Created:** `{created_date}`"
                f"\n> **Updated:** `{updated_date}`"
                f"\n> **Genre:** `{genre}`"
                f"\n> **Subgenre:** `{subgenre}`"
                f"{f'\n> **{emojis.emoji_dict.get('robux')}:** `{price}`' if price else ''}"
                f"\n> **Description:** ```{n_description} ```"
            ),
            inline=True
        )
        embed.add_field(
            name=(
                "Creator"
                f" {emojis.emoji_dict.get('verified_badge') if is_verified else ""}"
            ),
            value=(
                f"> **Name:** `{creator_name}`"
                f"\n> **Id:** `{creator_id}`"
                f"\n> **Type:** `{creator_type}`"
            ),
            inline=False
        )
        embed.set_thumbnail(
            url=thumbnail_url
        )
        await interaction.response.send_message(files=[file], embed=embed)

    @roblox_info.error
    @roblox_badges.error
    @roblox_outfit.error
    @roblox_place_info.error
    async def say_error(self, interaction: discord.Interaction, error):

        await interaction.response.send_message(embed=embeds.make_error_embed(error), ephemeral=True)

async def setup(bot):
    await bot.add_cog(robloxComands(bot))
