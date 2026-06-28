from .api_manager import get_api_data, post_api_data
import SECRETS

HEADER={'Cookie': f'.ROBLOSECURITY={SECRETS.ROBLOX_COOKIE}', 'x-api-key': SECRETS.ROLBOX_API_KEY}

# Informations
def get_player_profile(username: str = None, userId: int = None, excludeBannedUsers: bool = False):
    if username is None and userId is None: return
    if not userId:
        json = {
            "usernames": [username],
            "excludeBannedUsers": excludeBannedUsers,
        }
        data = post_api_data(f'https://users.roblox.com/v1/usernames/users', json=json).json().get("data", None)
        if not data or data == []: return
        userId = data[0].get('id')
    return get_api_data(f'https://users.roblox.com/v1/users/{userId}', headers=HEADER).json()

def get_player_username_history(userId: int, limit: int = 10, cursor: str = None, sortOrder: str = 'Asc'):
    '''
    Not functional. DO NOT USE.
    '''
    return get_api_data(f'https://users.roblox.com/v1/users/{userId}/username-history', headers=HEADER).json()

def get_user_presence(userId: int):
    json = {
        "userIds": [userId],
    }
    return post_api_data(f'https://presence.roblox.com/v1/presence/users', json=json).json()

def get_user_premium_membership(userId: int = None):
    return get_api_data(f'https://premiumfeatures.roblox.com/v1/users/{userId}/validate-membership', headers=HEADER).json()

def get_user_followers(userId: int):
    return get_api_data(f'https://friends.roblox.com/v1/users/{userId}/followers/count', headers=HEADER).json()

def get_user_followings(userId: int):
    return get_api_data(f'https://friends.roblox.com/v1/users/{userId}/followings/count', headers=HEADER).json()

# Thumbnails
def get_player_full_body(userId: int, size: str = '720x720', format: str = 'Png', isCircular: bool = False):
    params = {
        'userIds': userId,
        'size': size,
        'format': format,
        'isCircular': isCircular,
    }
    return get_api_data(f'https://thumbnails.roblox.com/v1/users/avatar', params=params, headers=HEADER).json()

def get_player_bust(userId: int, size: str = '420x420', format: str = 'Png', isCircular: bool = False):
    params = {
        'userIds': userId,
        'size': size,
        'format': format,
        'isCircular': isCircular,
    }
    return get_api_data(f'https://thumbnails.roblox.com/v1/users/avatar-bust', params=params, headers=HEADER).json()

def get_player_headshot(userId: int, size: str = '720x720', format: str = 'Png', isCircular: bool = False):
    params = {
        'userIds': userId,
        'size': size,
        'format': format,
        'isCircular': isCircular,
    }
    return get_api_data(f'https://thumbnails.roblox.com/v1/users/avatar-headshot', params=params, headers=HEADER).json()

def get_asset_thumbnail(assetId: int, size: str = '700x700', format: str = 'Png', isCircular: bool = False):
    params = {
        'assetIds': assetId,
        'returnPolicy': 'PlaceHolder',
        'size': size,
        'format': format,
        'isCircular': isCircular,
    }
    return get_api_data(f'https://thumbnails.roblox.com/v1/assets', params=params, headers=HEADER).json()

# Inventory
def get_ouftfit_details(userId: int = None):
    return get_api_data(f'https://avatar.roblox.com/v1/users/{userId}/avatar', headers=HEADER).json()

def get_player_badges(userId: int):
    return get_api_data(f'https://accountinformation.roblox.com/v1/users/{userId}/roblox-badges', headers=HEADER).json()
