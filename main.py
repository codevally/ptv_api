import os
import hmac
import requests
from hashlib import sha1
from dotenv import load_dotenv

load_dotenv()
base_url = 'https://timetableapi.ptv.vic.gov.au'

class PTVAPI:
    def __init__(self, user_id, api_key):
        self.user_id = user_id
        self.api_key = api_key

    def __call__(self, endpoint, **params):
        params['devid'] = self.user_id
        encoded = [f'{k}={v}'
                   for k, vs in params.items()
                   for v in (vs if isinstance(vs, (list, tuple)) else [vs])]

        request = f'{endpoint}?{"&".join(encoded)}'
        hashed = hmac.new(self.api_key.encode('utf-8'), request.encode('utf-8'), sha1)
        url = f'{base_url}{request}&signature={hashed.hexdigest()}'

        response = requests.get(url)
        response.raise_for_status()
        return response.json()

ptv = PTVAPI(os.getenv('USER_ID'), os.getenv('API_KEY'))
print(ptv('/v3/disruptions', route_types=2))

def main():
    print("Hello from ptv-api!")

if __name__ == "__main__":
    main()
