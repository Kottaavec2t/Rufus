import requests

def get_api_data_json(url: str, headers: dict = None, params: dict = None) -> dict | None:
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_e:
        print(f"HTTP error occurred: {http_e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_api_data_image(url: str, headers: dict = None):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.content
    
    except requests.exceptions.HTTPError as http_e:
        print(f"HTTP error occurred: {http_e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def post_api_data_json(url: str, json: dict = None):
    try:
        response = requests.post(url, json=json)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_e:
        print(f"HTTP error occurred: {http_e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# print(get_api_data_json(f'https://users.roblox.com/v1/users/{post_api_data_json(f'https://users.roblox.com/v1/usernames/users', {"usernames": ['Telamon'], "excludeBannedUsers": False})["data"][0]['id']}/username-history'))

