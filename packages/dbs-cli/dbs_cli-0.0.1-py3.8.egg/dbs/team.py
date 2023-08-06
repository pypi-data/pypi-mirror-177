import requests


BASE_URL = 'https://staging.api.labelr.io'


def get_team_detail(api_key):
    url = BASE_URL + '/team/v1/team-detail/'
    headers = {
        "Content-Type": "application/json",
        'X-ACCESS-KEY': api_key,
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()
