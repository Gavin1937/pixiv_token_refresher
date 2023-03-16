
import json
from pixiv_auth import (
    AUTH_TOKEN_URL, CLIENT_ID,
    CLIENT_SECRET, USER_AGENT,
    REQUESTS_KWARGS,
    print_auth_token_response
)
import requests


class refresher:
    
    def __init__(self):
        self.__token:str = None
        self.__load_token()
        pass
    
    # api
    def do_refresh(self, refresh_token:str=None) -> dict:
        if refresh_token is None:
            refresh_token = self.__token['refresh_token']
        
        try:
            resp = self.__refresh(refresh_token)
            respjson = resp.json()
            # print(json.dumps(resp, indent=2, ensure_ascii=False))
            self.__token = {
                'access_token': respjson['access_token'],
                'refresh_token': respjson['refresh_token'],
                'expires_in': respjson['expires_in']
            }
        except KeyError:
            print('Failed to refresh pixiv token.')
            exit(-1)
        except Exception as err:
            print(f'do_refresh() Exception: {err}')
        
        print_auth_token_response(resp)
        self.__write_token()
        return self.__token
    
    # private helper functions
    def __load_token(self):
        try:
            with open('token.json', 'r', encoding='utf-8') as file:
                self.__token = json.load(file)
        except Exception as err:
            print(f'Failed to load tokens. Exception: {err}')
            exit(-1)
    
    def __write_token(self):
        try:
            with open('token.json', 'w', encoding='utf-8') as file:
                json.dump(self.__token, file, indent=2, ensure_ascii=False)
        except Exception as err:
            print(f'Failed to write to token.json. Exception: {err}')
    
    # copy from pixiv_auth.py with a bit modification
    def __refresh(self, refresh_token) -> dict:
        response = requests.post(
            AUTH_TOKEN_URL,
            data={
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'grant_type': 'refresh_token',
                'include_policy': 'true',
                'refresh_token': refresh_token,
            },
            headers={
                'user-agent': USER_AGENT,
                'app-os-version': '14.6',
                'app-os': 'ios',
            },
            **REQUESTS_KWARGS
        )
        return response



if __name__ == '__main__':
    try:
        ref = refresher()
        ref.do_refresh()
    except Exception as err:
        print(err)
        exit(-1)

