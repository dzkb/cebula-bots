import requests


def discord_hook(hook_url, payload):
    response = requests.post(hook_url, json=payload)
    return response.status_code == 200
