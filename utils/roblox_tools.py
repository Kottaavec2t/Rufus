from .api_manager import get_api_data_json, post_api_data_json

def get_player_profile(username: str = None, userId: int = None, excludeBannedUsers: bool = False):
    if username is None and userId is None: return
    if not userId:
        userId = post_api_data_json(f'https://users.roblox.com/v1/usernames/users', {"usernames": [username], "excludeBannedUsers": excludeBannedUsers})["data"][0]['id']
    return get_api_data_json(f'https://users.roblox.com/v1/users/{userId}')

def get_player_badges(username: str = None, userId: int = None):
    if username is None and userId is None: return
    if not userId:
        userId = get_player_profile(username)["id"]
    return get_api_data_json(f'https://accountinformation.roblox.com/v1/users/{userId}/roblox-badges')

def get_player_promotion_channels(username: str = None, userId: int = None):
    if username is None and userId is None: return
    if not userId:
        userId = get_player_profile(username)["id"]
    return get_api_data_json(f'https://accountinformation.roblox.com/v1/users/{userId}/promotion-channels')

def get_player_username_history(username: str = None, userId: int = None, limit: int = 10, cursor: str = None, sortOrder: str = 'Asc'):
    '''
    Not functional. DO NOT USE.
    '''
    if username is None and userId is None: return
    if not userId:
        userId = get_player_profile(username)["id"]
    return get_api_data_json(f'https://users.roblox.com/v1/users/{userId}/username-history')