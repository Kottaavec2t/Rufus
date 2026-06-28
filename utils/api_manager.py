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

def post_api_data(url: str, json: dict = None, data: dict = None, headers: dict = None):
    try:
        response = requests.post(url, json=json, data=data, headers=headers)
        response.raise_for_status()
        return response
    
    except requests.exceptions.HTTPError as http_e:
        print(f"HTTP error occurred: {http_e}")
    except Exception as e:
        print(f"An error occurred: {e}")
