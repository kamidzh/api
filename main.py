import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import argparse


def shorten_link(token, long_url):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    params = {
        "long_url": long_url
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(token, bitlink):
    url_clicks = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    params = {
        'unit' : 'month',
        'units' : '-1'
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url_clicks, headers=headers, params=params)
    response.raise_for_status()
    total_clicks = response.json()['total_clicks']
    return total_clicks


def is_bitlink(token, url):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{url}'
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.ok

    
def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='счет кликов по ссылке')
    parser.add_argument('--url', help='введите ссылку')
    args = parser.parse_args()
    parsed_url = urlparse(args.url)
    parsed_url = f'{parsed_url.netloc}{parsed_url.path}'
    token = os.getenv("BITLY_TOKEN")
    try:
        if is_bitlink(token, parsed_url):
            print(count_clicks(token, parsed_url))
        else:
            print(shorten_link(token, args.url))
    except requests.exceptions.HTTPError as error:
        print('Проверьте вашу ссылку', error)


if __name__ == '__main__':
    main()
