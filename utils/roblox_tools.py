from .api_manager import get_api_data_json, post_api_data_json, get_api_data
import SECRETS

HEADER={'Cookie': f'.ROBLOSECURITY={SECRETS.ROBLOX_COOKIE}', 'x-api-key': SECRETS.ROLBOX_API_KEY}

def get_player_profile(username: str = None, userId: int = None, excludeBannedUsers: bool = False):
    if username is None and userId is None: return
    if not userId:
        userId = post_api_data_json(f'https://users.roblox.com/v1/usernames/users', {"usernames": [username], "excludeBannedUsers": excludeBannedUsers})["data"][0]['id']
    return get_api_data_json(f'https://users.roblox.com/v1/users/{userId}', headers=HEADER)

def get_player_badges(username: str = None, userId: int = None):
    if username is None and userId is None: return
    if not userId:
        userId = get_player_profile(username)["id"]
    return get_api_data_json(f'https://accountinformation.roblox.com/v1/users/{userId}/roblox-badges', headers=HEADER)

def get_player_promotion_channels(username: str = None, userId: int = None):
    if username is None and userId is None: return
    if not userId:
        userId = get_player_profile(username)["id"]
    return get_api_data_json(f'https://accountinformation.roblox.com/v1/users/{userId}/promotion-channels', headers=HEADER)

def get_player_username_history(username: str = None, userId: int = None, limit: int = 10, cursor: str = None, sortOrder: str = 'Asc'):
    '''
    Not functional. DO NOT USE.
    '''
    if username is None and userId is None: return
    if not userId:
        userId = get_player_profile(username)["id"]
    return get_api_data_json(f'https://users.roblox.com/v1/users/{userId}/username-history', headers=HEADER)

def get_player_full_body(username: str = None, userId: int = None, size: str = '720x720', format: str = 'Png', isCircular: bool = False):
    if username is None and userId is None: return
    if not userId:
        userId = get_player_profile(username)["id"]
    return get_api_data_json(f'https://thumbnails.roblox.com/v1/users/avatar', params={'userIds': userId, 'size': size, 'format': format, 'isCircular': isCircular}, headers=HEADER)

def get_player_bust(username: str = None, userId: int = None, size: str = '420x420', format: str = 'Png', isCircular: bool = False):
    if username is None and userId is None: return
    if not userId:
        userId = get_player_profile(username)["id"]
    return get_api_data_json(f'https://thumbnails.roblox.com/v1/users/avatar-bust', params={'userIds': userId, 'size': size,  'format': format, 'isCircular': isCircular}, headers=HEADER)

def get_player_headshot(username: str = None, userId: int = None, size: str = '720x720', format: str = 'Png', isCircular: bool = False):
    if username is None and userId is None: return
    if not userId:
        userId = get_player_profile(username)["id"]
    return get_api_data_json(f'https://thumbnails.roblox.com/v1/users/avatar-headshot', params={'userIds': userId, 'size': size, 'format': format, 'isCircular': isCircular}, headers=HEADER)

def get_ouftfit_details(username: str = None, userId: int = None):
    if username is None and userId is None: return
    if not userId:
        userId = get_player_profile(username)["id"]
    return get_api_data_json(f'https://avatar.roblox.com/v1/users/{userId}/avatar', headers=HEADER)

def get_asset_thumbnail(assetId: int = None, size: str = '700x700', format: str = 'Png', isCircular: bool = False):
    if assetId is None: return
    return get_api_data_json(f'https://thumbnails.roblox.com/v1/assets', params={'assetIds': assetId, 'returnPolicy': 'PlaceHolder', 'size': size, 'format': format, 'isCircular': isCircular}, headers=HEADER)

def get_user_presence(username: str = None, userId: int = None):
    if username is None and userId is None: return
    if not userId:
        userId = get_player_profile(username)["id"]
    return post_api_data_json(f'https://presence.roblox.com/v1/presence/users', json={"userIds": [userId]})

def get_user_premium_membership(username: str = None, userId: int = None):
    if username is None and userId is None: return
    if not userId:
        userId = get_player_profile(username)["id"]
    return get_api_data_json(f'https://premiumfeatures.roblox.com/v1/users/{userId}/validate-membership', headers=HEADER)

def get_user_followers(username: str = None, userId: int = None):
    if username is None and userId is None: return
    if not userId:
        userId = get_player_profile(username)["id"]
    return get_api_data_json(f'https://friends.roblox.com/v1/users/{userId}/followers/count', headers=HEADER)

def get_user_followings(username: str = None, userId: int = None):
    if username is None and userId is None: return
    if not userId:
        userId = get_player_profile(username)["id"]
    return get_api_data_json(f'https://friends.roblox.com/v1/users/{userId}/followings/count', headers=HEADER)
