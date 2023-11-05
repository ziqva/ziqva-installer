import requests
from bs4 import BeautifulSoup
import json
import math

host: str = 'https://srv-ziqlabs-1.my.id'
root: str = f'{host}/share'

def scan(app) -> object or None:
    name: str = app['name']
    prefix: str = app['prefix']
    print(f'Scanning data for app "{name}", please wait for a moment...')
    data: list = format_source(deep_scan(prefix))
    latest_version: int = 0
    download_url: str or None = None
    size_mb: int = 0
    filename: str = ''
    extension: str = ''

    expected_extension: str = 'zip'
    for row in data :
        if row['extension'] == expected_extension and row['version'] != None and (str.lower(prefix) in str.lower(row['file_name'])) :
            if row['version'] > latest_version :
                latest_version = row['version']
                download_url = row['download_url']
                size_mb = row['size_mb']
                filename = row['file_name']
                extension = row['extension']

    if download_url == None :
        return None

    return {
        'filename': filename,
        'size_mb': size_mb,
        'download': download_url,
        'extension': extension,
        'version': '.'.join(str(latest_version))
    }

def format_source(data_deep_scan: list) -> list:
    tmp: list = []
    for row in data_deep_scan:
        detail: object = get_detail(row['file_name'])
        tmp.append({
            "download_url": f'{host}{row["url"]}',
            "file_name": row['file_name'],
            "size_mb": row['mb_size'],
            "version": detail['version'],
            "extension": detail['extension']
        })
    return tmp


def get_detail(filename: str) -> object:
    version: int or None = None
    version_strs: list = filename.split(' ')[-1].split('.')
    version_strs_new: list = []

    for v in version_strs:
        try:
            int(v)
            version_strs_new.append(v)
        except:
            _ = None

    version = None if len(version_strs_new) <= 0 else int(''.join(version_strs_new))
    return {
        'version': version,
        'extension': filename.split('.')[-1]
    }


def deep_scan(prefix: str) -> list:
    collections: list = []
    currently_scannings: list = [root]
    new_currently_scannings: list = []
    while len(currently_scannings) > 0:
        new_currently_scannings = []
        print(f'Collecting {len(currently_scannings)} source...')
        for currently_scanning in currently_scannings:
            html: str = requests.get(currently_scanning).text
            try:
                json_data: str = json.loads(html.split('const data = ')[1].split('}];')[0] + '}]')
                for json_row in json_data:
                    if json_row['mb_size'] == "0.00":
                        new_currently_scannings.append(f'{host}{json_row["url"]}')
                    else:
                        collections.append(json_row)
            except Exception as err:
                err = None
        currently_scannings = new_currently_scannings
    return collections
