from .api_manager import post_api_data
from .gd_formatter import to_dict

def get_player_profile(username: str = None, user_id: int = None, account_id: int = None):
    if username is None and user_id is None and account_id is None: return
    if not account_id:
        data = {
            'secret': "Wmfd2893gb7",
            'str': str(username) if username else str(user_id)
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            "User-Agent": ""
        }
        account_id = to_dict(post_api_data(f'http://www.boomlings.com/database/getGJUsers20.php', data=data, headers=headers).text)[0].get('16', None) # AccountID
    data = {
        'secret': "Wmfd2893gb7",
        'targetAccountID': account_id
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "User-Agent": ""
    }
    return post_api_data(f'http://www.boomlings.com/database/getGJUserInfo20.php', data=data, headers=headers).text

def get_level_data(level_id: int):
    if level_id is None: return
    headers = {
        "User-Agent": ""
    }

    data = {
        "levelID": level_id,
        "secret": "Wmfd2893gb7"
    }

    return post_api_data('http://www.boomlings.com/database/downloadGJLevel22.php', data=data, headers=headers).text

def get_song_data(song_id: int):
    if song_id is None: return
    headers = {
        "User-Agent": ""
    }

    data = {
        "songID": song_id,
        "secret": "Wmfd2893gb7"
    }

    return post_api_data('http://www.boomlings.com/database/getGJSongInfo.php', data=data, headers=headers).text
