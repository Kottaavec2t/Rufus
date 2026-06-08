import requests

def get_api_data(url: str, headers: dict = None, params: dict = None):
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response
    
    except requests.exceptions.HTTPError as http_e:
        print(f"HTTP error occurred: {http_e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_api_data_json(url: str, headers: dict = None, params: dict = None):
    return get_api_data(url, headers=headers, params=params).json()

def get_api_data_image(url: str, headers: dict = None, params: dict = None):
    return get_api_data(url, headers=headers, params=params).content

def post_api_data(url: str, json: dict = None):
    try:
        response = requests.post(url, json=json)
        response.raise_for_status()
        return response
    
    except requests.exceptions.HTTPError as http_e:
        print(f"HTTP error occurred: {http_e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def post_api_data_json(url: str, json: dict = None):
    return post_api_data(url, json=json).json()
