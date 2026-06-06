from .api_manager import get_api_data_json, get_api_data_image
from .minecraft_skin_renderer import skin_to_2d
from PIL import Image
from io import BytesIO

def get_player_profile(username: str = None, UUID: str = None):
    if username is None and UUID is None: return
    return get_api_data_json(f'https://api.minecraftapi.net/v3/profile/{username if username else UUID}')

def get_player_skin(username: str = None, UUID: str = None):
    if username is None and UUID is None: return
    return get_api_data_image(f'https://api.minecraftapi.net/v3/profile/{username if username else UUID}/skin')

def get_player_avatar(username: str = None, UUID: str = None, size: int = 128, overlay: bool = True):
    if username is None and UUID is None: return
    return get_api_data_image(f'https://api.minecraftapi.net/v3/profile/{username if username else UUID}/avatar?size={size}&overlay={'true' if overlay else 'false'}')

def get_player_cape(username: str = None, UUID: str = None):
    if username is None and UUID is None: return
    return get_api_data_image(f'https://api.minecraftapi.net/v3/profile/{username if username else UUID}/capes/minecraft')

def get_player_skin_render(username: str = None, UUID: str = None):
    if username is None and UUID is None: return
    return skin_to_2d(Image.open(BytesIO(get_player_skin(username, UUID))))
