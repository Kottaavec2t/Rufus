from .api_manager import get_api_data_json, post_api_data_json
import SECRETS

# INITIALIZE SESSION
TOKEN = post_api_data_json(f'https://osu.ppy.sh/oauth/token', json={
    "client_id":     SECRETS.OSU_CLIENT_ID,
    "client_secret": SECRETS.OSU_API_KEY,
    "grant_type":    "client_credentials",
    "scope":         "public",
})['access_token']
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}

def get_player_profile(username: str = None, user_id: int = None, gamemode: str = 'osu'):
    if username is None and user_id is None: return
    return get_api_data_json(f'https://osu.ppy.sh/api/v2/users/{username if username else user_id}/{gamemode}', headers=HEADERS)
