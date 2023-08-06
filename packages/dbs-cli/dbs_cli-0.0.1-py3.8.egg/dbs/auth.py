import requests
import os


BASE_URL = 'https://api.labelr.io'
CLIENT_ID = os.environ.get("DBS_CLI_CLIENT_ID")
CLIENT_SECRET = os.environ.get("DBS_CLI_CLIENT_SECRET")


def get_token(username, password):
    assert CLIENT_ID, 'Set environment variable: DBS_CLI_CLIENT_ID'
    assert CLIENT_SECRET, 'Set environment variable: DBS_CLI_CLIENT_SECRET'

    url = BASE_URL + '/auth/oauth/token/'
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }

    body = {
       "grant_type": "password",
       "username": username,
       "password": password,
       "client_id": CLIENT_ID,
       "client_secret": CLIENT_SECRET,
    }

    r = requests.post(url, data=body, headers=headers)
    r.raise_for_status()
    return r.json()


def refresh_token(refresh_token):
    assert CLIENT_ID, 'Set environment variable: DBS_CLI_CLIENT_ID'
    assert CLIENT_SECRET, 'Set environment variable: DBS_CLI_CLIENT_SECRET'

    url = BASE_URL + '/auth/oauth/token/'
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }

    body = {
       "grant_type": "refresh_token",
       "refresh_token": refresh_token,
       "client_id": CLIENT_ID,
       "client_secret": CLIENT_SECRET,
    }

    r = requests.post(url, data=body, headers=headers)
    r.raise_for_status()
    return r.json()


def get_user_profile(access_token):
    url = BASE_URL + f'/auth/profile/'
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Bearer {access_token}',
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()
